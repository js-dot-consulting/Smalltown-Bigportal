# Data

Every piece of data in this repo has to be traceable: where it came from, under what license, and how someone else could get the same thing.
That applies to the data we provide and to anything your team adds.
The one exception is the script that generates the Fergie seed: we keep it private, because it would give away what the judging walkthrough looks for. The seed files themselves are listed and checksummed like everything else.

## The rule

**AI can write the script that gets the data. It can't write the data.**

Use AI as much as you like to write fetch scripts, importers, converters and generators.
Don't let it type records into a file, fill gaps with plausible-looking facts, or "make the directory look fuller."
Data an AI made up looks exactly like real data, and nobody, including you, can tell them apart later.

Every dataset is one of three kinds:

| Kind | What it is | What it needs |
|---|---|---|
| `fetched` | Pulled from a real source by a script | The source, its license, the date you retrieved it, and the script. Each record says where it came from. |
| `synthetic` | Made up on purpose, by a script that always produces the same output | The script, and `"fictional": true`. Anyone who re-runs the script gets identical files. |
| `hand_entered` | Typed in by a person, in small amounts | A source on every record, like a photo of a flyer, a page URL or "the owner told us on Nov 28". |

## What's here

| Folder | What it contains | Kind |
|---|---|---|
| [seed/](seed/README.md) | The fictional town of Fergie. **Your demo must run on this.** | `synthetic` |
| [open/](open/) | Real, openly licensed data that fills gaps the seed doesn't cover: ten public-domain artworks from The Met, credited to their real makers, and group-level 2021 Census counts that weight Fergie's population mix. | `fetched` |
| [manifest.json](manifest.json) | The list of every dataset, its kind, source, license, script and checksums | |
| [check_data.py](check_data.py) | Checks the manifest against what's actually in the repo | |

The seed doesn't cover everything, on purpose.
Where it stops, look for open data that already exists before you make anything up.
[docs/resources.md](../docs/resources.md) lists sources we've checked, with their licenses.

## Adding your own data

1. Put it under `data/`, in a folder of your own, like `data/team/`.
2. If it's fetched or synthetic, commit the script that makes it, next to it.
3. Add an entry to [manifest.json](manifest.json). Copy one of ours as a starting point.
4. Run `python data/check_data.py --write-checksums`, then `python data/check_data.py`.
5. Fix anything it flags.

Real people's personal information never goes in, whatever its source.

### Manifest fields

| Field | Needed for | Notes |
|---|---|---|
| `id` | all | Short name for the dataset |
| `kind` | all | `fetched`, `synthetic` or `hand_entered` |
| `description` | all | One or two plain sentences |
| `files` | all | Paths from the repo root |
| `license` | all | The license the data is under. Add `license_url` where there is one |
| `script` | fetched, synthetic | Path from the repo root. Must run with `python <script>` from the repo root. The Fergie seed is the only dataset without one |
| `source_name`, `source_url`, `retrieved` | fetched | Who published it, where, and the date you got it |
| `fictional` | synthetic | Must be `true` |
| `record_source_field` | hand_entered, and recommended for fetched | The field on each record that says where it came from |
| `records_key` | optional | Where the list of records sits inside a JSON file, like `works` |
| `checksums` | all | Written for you by `--write-checksums` |

If your scripts aren't Python, wrap them in a short Python script that calls them, so the checker can re-run everything the same way.

## How judges use this

Before judging, we run `check_data.py` on every submission, re-run the synthetic scripts, and spot-check a sample of fetched and hand-entered records against their sources.

Data that isn't in the manifest, doesn't match its checksum, or can't be traced to its source gets **flagged**.
For each flag, the judge decides whether to leave out whatever depends on that data when scoring, or to score it down.
See "Data checks" in [JUDGING.md](../JUDGING.md).
