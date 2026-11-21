# Resources

Data sources, APIs and tools you might use.

Nothing here is required.
Building your own or using something not listed are both fine.

**Check the terms before you use anything.**
Some data can be displayed but not stored, some needs attribution, and some can't be used commercially.
The "Terms" column is a summary, not legal advice. Read the source.

Terms were checked against each source's own pages on 2026-11-21. They can change, and the terms in force when you download something are the ones that apply.

Whatever you use, list it in `data/manifest.json` with its source, license and the script that fetched it. See [data/README.md](../data/README.md).

---

## Data sources

**Licenses often differ item by item**, even inside one source.
Use only items whose own license field says what the "Terms" column says, and record that license in your manifest.

| Source | What it has | Terms | Link |
|---|---|---|---|
| OpenStreetMap | Streets, buildings, places and points of interest | ODbL 1.0. Commercial use is fine. Credit "© OpenStreetMap contributors" with a link to openstreetmap.org/copyright, and print that URL on printed maps. **Share-alike:** any OSM data you change and publish stays under ODbL, so give it its own folder and license file. Maps and prints made from it can be sold under any terms | [openstreetmap.org/copyright](https://www.openstreetmap.org/copyright) |
| Statistics Canada, 2021 Census Profile | Population, age, households, income and language for real towns and areas. Group-level only | Statistics Canada Open Licence. Commercial use is fine. Credit: "Source: Statistics Canada, *product name*, *reference date*." (or "Adapted from…" if you changed it). Don't combine it with other data to identify anyone. Downloads may need a browser | [Licence](https://www.statcan.gc.ca/en/reference/licence) · [Dataset](https://open.canada.ca/data/en/dataset/750e6035-adf8-4426-966f-4c25b12a999e) |
| Ontario Data Catalogue | Provincial datasets: places, services, environment, and more | Use only datasets marked **Open Government Licence – Ontario** and access level **open**. Many others are under review, restricted or under different terms. Credit: "Contains information licensed under the Open Government Licence – Ontario." | [data.ontario.ca](https://data.ontario.ca/) · [Licence](https://www.ontario.ca/page/open-government-licence-ontario) |
| Open Government Portal (Canada) | Federal datasets | Open Government Licence – Canada for most datasets, but check each one. Credit: "Contains information licensed under the Open Government Licence – Canada." | [open.canada.ca](https://open.canada.ca/en/open-government-licence-canada) |
| The Met Open Access | Artworks, with images for public-domain works | CC0 for the data, and for images where `isPublicDomain` is true. Commercial use is fine. Credit is requested, not required. Don't use Met trademarks or imply endorsement. We already fetched ten works into [data/open/](../data/open/) | [metmuseum.github.io](https://metmuseum.github.io/) |
| Art Institute of Chicago | Artworks, with images for public-domain works | Data is CC0, except the `description` field, which is CC BY 4.0. Images are CC0 only where `is_public_domain` is true. Requested caption: "Artist. Title, Date. The Art Institute of Chicago." Weekly data dumps on GitHub | [api.artic.edu/docs](https://api.artic.edu/docs/) |
| Smithsonian Open Access | Millions of objects, images and records | Use only items marked CC0. The API needs a free api.data.gov key | [API docs](https://edan.si.edu/openaccess/apidocs/) |
| Wikimedia Commons | Photos, maps, art and audio | Varies by file: CC BY, CC BY-SA, CC0, public domain. Commercial use is allowed for everything on Commons, but follow each file's credit and share-alike terms. Photos of people may need their consent for commercial use. Confirm the license on the file's page | [Reusing content](https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia) |
| Free Music Archive | Music | Varies by track. For anything you sell, use only CC BY, CC BY-SA, CC BY-ND or CC0. Never the NC tracks or "FMA-Limited". **No API and no hotlinking.** Download and host the files yourself | [License guide](https://freemusicarchive.org/License_Guide) |
| Standard Ebooks | Public-domain books | The editing is CC0, but the books are only "believed" public domain **in the US**. Canada's term is longer, so check each author, or stick to authors who died long ago | [standardebooks.org](https://standardebooks.org/ebooks) |

---

## APIs and services

| Service | What it does | Free tier or terms | Link |
|---|---|---|---|
| Environment and Climate Change Canada weather API | Current conditions, forecasts, climate history and air quality | Free, no key. ECCC's own end-use licence, not the Open Government Licence. Credit "Data Source: Environment and Climate Change Canada." Show weather alerts word for word. Send a meaningful User-Agent | [api.weather.gc.ca](https://api.weather.gc.ca/) · [Licence](https://eccc-msc.github.io/open-data/licence/readme_en/) |
| OpenStreetMap tiles | Map images for a live map | Free, best effort, no guarantee. Show attribution, send a real User-Agent, and don't bulk download or use offline. Fine for a demo. For anything serious, use another OSM-based tile provider | [Tile usage policy](https://operations.osmfoundation.org/policies/tiles/) |
| Wikimedia Commons API | Reads a file's license, author and credit | Free, no key. Send a descriptive User-Agent and make requests one at a time. License fields can be missing, so confirm on the file page | [CommonsMetadata](https://www.mediawiki.org/wiki/Extension:CommonsMetadata) |

---

## Standards and references

- [schema.org](https://schema.org): structured data types for local businesses, events and offers.
- [Google Rich Results Test](https://search.google.com/test/rich-results): shows what search engines actually read from a page.
- [Model Context Protocol](https://modelcontextprotocol.io): an open standard for connecting AI tools to data and actions.
