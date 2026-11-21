"""Fetch a small set of public-domain artworks from The Met's Open Access collection.

These works are real, by real makers, and are credited to them. They are NOT
works by Fergie's creators. They stand in for "art on the site" so teams can
build galleries, credit lines and print products on something real, instead of
inventing art or generating it with AI.

Source:   The Metropolitan Museum of Art Collection API
          https://metmuseum.github.io/
License:  Data, and images of works flagged isPublicDomain, are CC0 1.0
          https://metmuseum.github.io/ and
          https://github.com/metmuseum/openaccess

The object IDs below are a fixed list, so anyone can re-run this script and
check every record against the same source.

Run from anywhere:  python data/open/fetch_met_works.py
Needs Python 3 and its standard library, plus an internet connection.
"""

import json
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

OUT = Path(__file__).resolve().parent / "met_works.json"
API = "https://collectionapi.metmuseum.org/public/collection/v1/objects/{}"
LICENSE = "CC0 1.0 (The Met Open Access)"
LICENSE_URL = "https://creativecommons.org/publicdomain/zero/1.0/"

# Chosen to echo things Fergie cares about: quilts, Scottish roots, a river
# and its mill, harvest and the market, summer theatre, stone bridges, pipers.
# Some have no known maker on purpose: credit should show that honestly.
OBJECT_IDS = [
    855672,  # Quilt, appliqued, ca. 1860
    854567,  # Quilt, pieced, ca. 1850
    857566,  # The Cuillin Hills, Isle of Skye (Paul Jacob Naftel)
    382933,  # Near Blair Athol, Scotland (J. M. W. Turner)
    415909,  # Mill River Scenery (Frances Flora Bond Palmer)
    11123,   # Harvest Scene (Winslow Homer)
    205100,  # Harvest jug (Robert Burnal of Cutcombe)
    739712,  # Salanio, Salerio and Shylock (John Massey Wright)
    427722,  # The Horseman on the Stone Bridge (Allart van Everdingen)
    201608,  # Bagpipe player, ceramic
]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "smalltown-bigportal-seed/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def blank_to_none(value):
    value = (value or "").strip()
    return value or None


def record(obj, retrieved):
    oid = obj["objectID"]
    return {
        "id": f"met_{oid}",
        "title": blank_to_none(obj.get("title")),
        "maker": blank_to_none(obj.get("artistDisplayName")),  # null means unknown maker
        "maker_bio": blank_to_none(obj.get("artistDisplayBio")),
        "date": blank_to_none(obj.get("objectDate")),
        "medium": blank_to_none(obj.get("medium")),
        "classification": blank_to_none(obj.get("classification")),
        "department": blank_to_none(obj.get("department")),
        "museum_credit_line": blank_to_none(obj.get("creditLine")),
        "image_small_url": blank_to_none(obj.get("primaryImageSmall")),
        "image_url": blank_to_none(obj.get("primaryImage")),
        "object_url": blank_to_none(obj.get("objectURL")),
        "license": LICENSE,
        "license_url": LICENSE_URL,
        "open_to_selling_prints": True,  # public domain: anyone may sell prints
        "source": {
            "name": "The Metropolitan Museum of Art Collection API",
            "url": API.format(oid),
            "as_of": retrieved,
        },
    }


def main():
    retrieved = date.today().isoformat()
    works = []
    for oid in OBJECT_IDS:
        obj = get(API.format(oid))
        if not obj.get("isPublicDomain"):
            sys.exit(f"Object {oid} is not public domain. Remove it from OBJECT_IDS.")
        works.append(record(obj, retrieved))
        time.sleep(0.2)  # be gentle with the API

    data = {
        "about": (
            "Real public-domain artworks from The Met, credited to their real makers. "
            "They are not by Fergie's creators. Use them as stand-ins for art on the site, "
            "and keep the maker and museum credit wherever a work appears."
        ),
        "retrieved": retrieved,
        "works": works,
    }
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Wrote {len(works)} works to {OUT}")


if __name__ == "__main__":
    main()
