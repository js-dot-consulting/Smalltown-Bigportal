"""Fetch group-level 2021 Census counts for Centre Wellington, Ontario.

Fergie is fictional. Its synthetic town generator needs believable proportions
for things like age, household type and how people get to work, and inventing
those would break the data rule. So this script pulls the real aggregate counts
for one real small Ontario township, Centre Wellington, and writes them as
weights. They are counts for whole groups (thousands of people), never
individual-level data. Fergie is not Centre Wellington: the generator only
uses the shape of these numbers.

Source:   Statistics Canada, Census Profile, 2021 Census of Population,
          via the Census Profile Web Data Service (SDMX REST API)
          https://www12.statcan.gc.ca/wds-sdw/2021profile-profil2021-eng.cfm
License:  Statistics Canada Open Licence
          https://www.statcan.gc.ca/en/reference/licence
Credit:   Adapted from Statistics Canada, Census Profile, 2021 Census of Population.

How it works:
  1. Look up the census subdivision's DGUID in the CL_GEO_CSD code list by its
     exact StatCan description, so the code isn't typed in by hand.
  2. Download the CL_CHARACTERISTIC code list (names and parent rows).
  3. Download every count for that DGUID (gender = Total, statistic = Counts).
  4. Add up the rows listed in BUCKETS below. Each row is checked by ID, by its
     exact name and by the census table it sits in, so if StatCan renumbers
     anything the bucket is skipped with a warning instead of being wrong.
  5. Write census_weights.json, with every number traced to its census rows
     under "characteristics".

Notes on the numbers:
  - StatCan randomly rounds Census Profile counts to a multiple of 5, so
    sub-rows don't always add up exactly to their total. The summary shows how
    far off each group is.
  - Most groups (tenure, mobility, labour, commuting) come from the 25% sample;
    age, household type and home language are 100% data.
  - The Census Profile has no single years of age, so "18-24" is "20 to 24"
    plus 2/5 of "15 to 19" (assumes ages 15-19 are evenly spread). This is
    recorded in "characteristics".

Run from anywhere:  python data/open/fetch_census_weights.py
Needs Python 3 and its standard library, plus an internet connection.
"""

import csv
import io
import json
import re
import sys
import urllib.request
from datetime import date
from fractions import Fraction
from pathlib import Path

OUT = Path(__file__).resolve().parent / "census_weights.json"
USER_AGENT = "Smalltown-Bigportal-track-data/1.0"

SDMX = "https://api.statcan.gc.ca/census-recensement/profile/sdmx/rest"
GEO_CODELIST_URL = f"{SDMX}/codelist/STC_CP/CL_GEO_CSD/latest"
CHAR_CODELIST_URL = f"{SDMX}/codelist/STC_CP/CL_CHARACTERISTIC/latest"
# Key = FREQ.REF_AREA.GENDER.CHARACTERISTIC.STATISTIC.
# A5 = census year, GENDER 1 = Total, CHARACTERISTIC empty = all, STATISTIC 1 = Counts.
DATA_URL = f"{SDMX}/data/STC_CP,DF_CSD/A5.{{dguid}}.1..1"

STRUCTURE_JSON = "application/vnd.sdmx.structure+json;version=1.0"
DATA_CSV = "application/vnd.sdmx.data+csv;version=1.0.0"

GEO_DESCRIPTION = "Centre Wellington, Township [Census subdivision], Ontario"

LICENSE = "Statistics Canada Open Licence"
LICENSE_URL = "https://www.statcan.gc.ca/en/reference/licence"
SOURCE_NAME = "Statistics Canada, Census Profile, 2021 Census of Population"
CREDIT = "Adapted from Statistics Canada, Census Profile, 2021 Census of Population."

# Census tables (top-level "Total - ..." rows) by ID, with their exact names.
# Every bucket row must sit under the table named for its group.
T_AGE = ("8", "Total - Age groups of the population - 100% data")
T_HOUSEHOLD = ("100", "Total - Household type - 100% data")
T_TENURE = ("1400", "Total - Private households by tenure - 25% sample data")
T_MOBILITY5 = ("1969", "Total - Mobility status 5 years ago - 25% sample data")
T_WORKPLACE = ("2593", "Total - Place of work status for the employed labour force aged 15 years and over - 25% sample data")
T_DESTINATION = ("2598", "Total - Commuting destination for the employed labour force aged 15 years and over with a usual place of work - 25% sample data")
T_MODE = ("2603", "Total - Main mode of commuting for the employed labour force aged 15 years and over with a usual place of work or no fixed workplace address - 25% sample data")
T_LABOUR = ("2223", "Total - Population aged 15 years and over by labour force status - 25% sample data")
T_HOME_LANGUAGE = ("721", "Total - Language spoken most often at home for the total population excluding institutional residents - 100% data")
POPULATION_2021 = ("1", "Population, 2021")

# group -> (table, {bucket: [(characteristic ID, exact name, share), ...]})
# share is the fraction of that row to count; 1 everywhere except the 18-24
# approximation.
ONE = Fraction(1)
BUCKETS = {
    "age_band": (T_AGE, {
        "18-24": [("15", "20 to 24 years", ONE), ("14", "15 to 19 years", Fraction(2, 5))],
        "25-34": [("16", "25 to 29 years", ONE), ("17", "30 to 34 years", ONE)],
        "35-44": [("18", "35 to 39 years", ONE), ("19", "40 to 44 years", ONE)],
        "45-54": [("20", "45 to 49 years", ONE), ("21", "50 to 54 years", ONE)],
        "55-64": [("22", "55 to 59 years", ONE), ("23", "60 to 64 years", ONE)],
        "65-74": [("25", "65 to 69 years", ONE), ("26", "70 to 74 years", ONE)],
        "75+": [("27", "75 to 79 years", ONE), ("28", "80 to 84 years", ONE), ("29", "85 years and over", ONE)],
    }),
    "household_type": (T_HOUSEHOLD, {
        "one_person": [("110", "One-person households", ONE)],
        "couple_no_children": [("104", "Without children", ONE)],
        "couple_with_children": [("103", "With children", ONE)],
        "one_parent": [("105", "One-parent-family households", ONE)],
        "multigenerational": [("106", "Multigenerational households", ONE)],
        "other": [
            ("107", "Multiple-census-family households", ONE),
            ("108", "One-census-family households with additional persons", ONE),
            ("109", "Two-or-more-person non-census-family households", ONE),
        ],
    }),
    "tenure": (T_TENURE, {
        "own": [("1401", "Owner", ONE)],
        "rent": [("1402", "Renter", ONE)],
    }),
    "mobility_5yr": (T_MOBILITY5, {
        "non_movers": [("1970", "Non-movers", ONE)],
        # StatCan "non-migrants" moved but stayed in the same census subdivision.
        "moved_within_csd": [("1972", "Non-migrants", ONE)],
        # "Migrants" moved in from another subdivision, province or country.
        "moved_from_elsewhere": [("1973", "Migrants", ONE)],
    }),
    "work_location": (T_WORKPLACE, {
        "usual_place": [("2597", "Usual place of work", ONE)],
        "worked_at_home": [("2594", "Worked at home", ONE)],
        "no_fixed_address": [("2596", "No fixed workplace address", ONE)],
        "outside_canada": [("2595", "Worked outside Canada", ONE)],
    }),
    "commute_destination": (T_DESTINATION, {
        "within_csd": [("2599", "Commute within census subdivision (CSD) of residence", ONE)],
        "different_csd_same_cd": [("2600", "Commute to a different census subdivision (CSD) within census division (CD) of residence", ONE)],
        "different_cd": [("2601", "Commute to a different census subdivision (CSD) and census division (CD) within province or territory of residence", ONE)],
        "other": [("2602", "Commute to a different province or territory", ONE)],
    }),
    "commute_mode": (T_MODE, {
        "car_driver": [("2605", "Car, truck or van - as a driver", ONE)],
        "car_passenger": [("2606", "Car, truck or van - as a passenger", ONE)],
        "public_transit": [("2607", "Public transit", ONE)],
        "walked": [("2608", "Walked", ONE)],
        "bicycle": [("2609", "Bicycle", ONE)],
        "other": [("2610", "Other method", ONE)],
    }),
    "labour_force": (T_LABOUR, {
        "employed": [("2225", "Employed", ONE)],
        "unemployed": [("2226", "Unemployed", ONE)],
        "not_in_labour_force": [("2227", "Not in the labour force", ONE)],
    }),
}

# Home language: English and French rows, then the most common individual
# non-official languages under this row (single responses only).
LANG_ENGLISH = ("724", "English")
LANG_FRENCH = ("725", "French")
LANG_NON_OFFICIAL = ("726", "Non-official languages")
TOP_NON_OFFICIAL = 5

# Census language name -> ISO 639-1 code. A lookup table, not data: languages
# without a two-letter code (or not listed here) get a lowercase slug instead.
ISO_639_1 = {
    "Afrikaans": "af", "Albanian": "sq", "Amharic": "am", "Arabic": "ar",
    "Armenian": "hy", "Bengali": "bn", "Bosnian": "bs", "Bulgarian": "bg",
    "Burmese": "my", "Croatian": "hr", "Czech": "cs", "Danish": "da",
    "Dutch": "nl", "Estonian": "et", "Finnish": "fi", "German": "de",
    "Greek": "el", "Gujarati": "gu", "Hebrew": "he", "Hindi": "hi",
    "Hungarian": "hu", "Icelandic": "is", "Indonesian": "id", "Italian": "it",
    "Japanese": "ja", "Khmer (Cambodian)": "km", "Korean": "ko",
    "Kurdish": "ku", "Lao": "lo", "Latvian": "lv", "Lithuanian": "lt",
    "Macedonian": "mk", "Malay": "ms", "Malayalam": "ml", "Maltese": "mt",
    "Marathi": "mr", "Nepali": "ne", "Norwegian": "no", "Pashto": "ps",
    "Persian (Farsi)": "fa", "Polish": "pl", "Portuguese": "pt",
    "Punjabi (Panjabi)": "pa", "Romanian": "ro", "Russian": "ru",
    "Serbian": "sr", "Sinhala (Sinhalese)": "si", "Slovak": "sk",
    "Slovene (Slovenian)": "sl", "Somali": "so", "Spanish": "es",
    "Swahili": "sw", "Swedish": "sv", "Tagalog (Pilipino, Filipino)": "tl",
    "Tamil": "ta", "Telugu": "te", "Thai": "th", "Tigrigna": "ti",
    "Turkish": "tr", "Ukrainian": "uk", "Urdu": "ur", "Vietnamese": "vi",
    "Welsh": "cy", "Yiddish": "yi", "Yoruba": "yo",
}

warnings = []


def warn(msg):
    warnings.append(msg)
    print(f"WARNING: {msg}", file=sys.stderr)


def get(url, accept):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8")


def codes(structure_text, codelist_id):
    """Return {code id: code dict} for one code list in an SDMX-JSON structure message."""
    for cl in json.loads(structure_text)["data"]["codelists"]:
        if cl.get("id") == codelist_id:
            return {str(c["id"]): c for c in cl["codes"]}
    sys.exit(f"Code list {codelist_id} not found in the response.")


def find_dguid():
    geo = codes(get(GEO_CODELIST_URL, STRUCTURE_JSON), "CL_GEO_CSD")
    hits = [cid for cid, c in geo.items() if c.get("description") == GEO_DESCRIPTION]
    if len(hits) != 1:
        sys.exit(f"Expected one CSD described as {GEO_DESCRIPTION!r}, found {len(hits)}.")
    return hits[0], geo[hits[0]]


def load_values(dguid):
    url = DATA_URL.format(dguid=dguid)
    rows = csv.DictReader(io.StringIO(get(url, DATA_CSV)))
    values = {}
    for r in rows:
        if (r.get("REF_AREA"), r.get("GENDER"), r.get("STATISTIC")) != (dguid, "1", "1"):
            sys.exit(f"Unexpected row in response: {r.get('REF_AREA')}/{r.get('GENDER')}/{r.get('STATISTIC')}")
        cid = r["CHARACTERISTIC"]
        if cid in values:
            sys.exit(f"Characteristic {cid} appears twice in the response.")
        values[cid] = (r.get("OBS_VALUE", "").strip(), r.get("FLAG", "").strip())
    if not values:
        sys.exit("The data response had no rows.")
    return url, values


class Profile:
    def __init__(self, chars, values):
        self.chars = chars
        self.values = values

    def name(self, cid):
        return self.chars.get(cid, {}).get("name")

    def root(self, cid):
        seen = set()
        while self.chars.get(cid, {}).get("parent") and cid not in seen:
            seen.add(cid)
            cid = self.chars[cid]["parent"]
        return cid

    def count(self, cid, expected_name, table=None):
        """Return the integer count for one row, or None (with a warning) if it isn't what we expect."""
        actual = self.name(cid)
        if actual != expected_name:
            warn(f"Characteristic {cid} is named {actual!r}, expected {expected_name!r}")
            return None
        if table and self.root(cid) != table[0]:
            warn(f"Characteristic {cid} ({expected_name}) is not under table {table[0]} ({table[1]})")
            return None
        raw, flag = self.values.get(cid, ("", ""))
        if flag or not re.fullmatch(r"\d+", raw):
            warn(f"Characteristic {cid} ({expected_name}) has no usable count (value {raw!r}, flag {flag!r})")
            return None
        return int(raw)

    def table_total(self, table):
        cid, name = table
        if self.root(cid) != cid:
            warn(f"Characteristic {cid} is not a top-level table")
            return None
        return self.count(cid, name)


def trace(cid, name, share, table):
    label = f"[{cid}] {name}"
    if share != 1:
        label += f" x {share} (approximation: the Census Profile has no single years of age, so ages 15-19 are assumed evenly spread)"
    return f"{label} | {table[1]}"


def build_group(profile, table, buckets, characteristics, group):
    out = {}
    for bucket, parts in buckets.items():
        total = Fraction(0)
        for cid, name, share in parts:
            n = profile.count(cid, name, table)
            if n is None:
                total = None
                break
            total += n * share
        if total is None:
            warn(f"Skipping {group}.{bucket}")
            continue
        out[bucket] = round(total)
        characteristics[f"{group}.{bucket}"] = [trace(cid, name, share, table) for cid, name, share in parts]
    return out


def slug(name):
    return re.sub(r"[^a-z0-9]+", "_", re.sub(r"\(.*?\)", "", name).lower()).strip("_")


def build_languages(profile, characteristics):
    table = T_HOME_LANGUAGE
    out = {}
    for key, (cid, name) in (("en", LANG_ENGLISH), ("fr", LANG_FRENCH)):
        n = profile.count(cid, name, table)
        if n is None:
            warn(f"Skipping language_home.{key}")
            continue
        out[key] = n
        characteristics[f"language_home.{key}"] = [trace(cid, name, ONE, table)]

    # Every leaf row (a single language, not a language family) below
    # "Non-official languages" in this table.
    if profile.count(*LANG_NON_OFFICIAL, table) is None:
        warn("Skipping non-official home languages")
        return out
    children = {}
    for cid, c in profile.chars.items():
        if c.get("parent"):
            children.setdefault(c["parent"], []).append(cid)
    leaves, stack = [], [LANG_NON_OFFICIAL[0]]
    while stack:
        cid = stack.pop()
        kids = children.get(cid, [])
        if kids:
            stack.extend(kids)
        else:
            leaves.append(cid)
    counted = []
    for cid in leaves:
        name = profile.name(cid)
        n = profile.count(cid, name, table)
        if n:
            counted.append((n, cid, name))
    counted.sort(key=lambda t: (-t[0], int(t[1])))
    for n, cid, name in counted[:TOP_NON_OFFICIAL]:
        key = ISO_639_1.get(name) or slug(name)
        if key in out:
            key = f"{key}_{cid}"
        out[key] = n
        characteristics[f"language_home.{key}"] = [trace(cid, name, ONE, table)]
    return out


def main():
    retrieved = date.today().isoformat()

    dguid, geo = find_dguid()
    chars = codes(get(CHAR_CODELIST_URL, STRUCTURE_JSON), "CL_CHARACTERISTIC")
    data_url, values = load_values(dguid)
    profile = Profile(chars, values)

    population = profile.count(*POPULATION_2021)
    if population is None:
        sys.exit("Could not read the 2021 population.")

    characteristics = {"geography.population_2021": [f"[{POPULATION_2021[0]}] {POPULATION_2021[1]}"]}
    weights = {}
    checks = []
    for group, (table, buckets) in BUCKETS.items():
        weights[group] = build_group(profile, table, buckets, characteristics, group)
        checks.append((group, table))
    weights["language_home"] = build_languages(profile, characteristics)
    # Re-order so language_home sits where the README's shape puts it.
    order = ["age_band", "household_type", "tenure", "language_home", "mobility_5yr",
             "work_location", "commute_destination", "commute_mode", "labour_force"]
    weights = {k: weights[k] for k in order}

    data = {
        "source_name": SOURCE_NAME,
        "source_url": data_url,
        "lookup_urls": [GEO_CODELIST_URL, CHAR_CODELIST_URL],
        "license": LICENSE,
        "license_url": LICENSE_URL,
        "credit": CREDIT,
        "geography": {
            "name": geo.get("name"),
            "type": "Township (census subdivision)",
            "dguid": dguid,
            "province": "Ontario",
            "population_2021": population,
        },
        "retrieved": retrieved,
        "note": (
            "Group-level counts used only as weights for a fictional town. "
            "Fergie is not Centre Wellington."
        ),
        "rounding_note": (
            "StatCan randomly rounds Census Profile counts to a multiple of 5, so buckets "
            "may not sum exactly to their table total. Most groups are 25% sample data; "
            "age, household type and home language are 100% data."
        ),
        "weights": weights,
        "characteristics": characteristics,
    }
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # Summary
    print(f"{geo.get('description')}  DGUID {dguid}  population 2021: {population:,}")
    for group, table in checks:
        total = profile.table_total(table)
        got = sum(weights[group].values())
        if total is not None and group == "age_band":
            # Bands start at 18, so compare with all ages minus 0-14 and 3/5 of 15-19.
            under_15 = profile.count("9", "0 to 14 years", table)
            age_15_19 = profile.count("14", "15 to 19 years", table)
            if under_15 is not None and age_15_19 is not None:
                total = round(total - under_15 - Fraction(3, 5) * age_15_19)
        diff = "" if total is None else f"  (table total {total:,}, diff {got - total:+,})"
        if group == "age_band":
            diff = diff.replace("table total", "estimated 18+")
        print(f"  {group:20s} {got:>7,}{diff}")
        for bucket, n in weights[group].items():
            print(f"      {bucket:24s} {n:>7,}")
    lang = weights["language_home"]
    lang_total = profile.table_total(T_HOME_LANGUAGE)
    print(f"  {'language_home':20s} {sum(lang.values()):>7,}  (of {lang_total:,}; rest are other languages and multiple responses)")
    for bucket, n in lang.items():
        print(f"      {bucket:24s} {n:>7,}")
    print(f"Wrote {OUT}")
    if warnings:
        print(f"{len(warnings)} warning(s); see above.")


if __name__ == "__main__":
    main()
