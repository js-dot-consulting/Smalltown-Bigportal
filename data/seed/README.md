# Seed data: the town of Fergie

Starting data so you can build on the first morning instead of collecting data.

Your demo must run on it. Extend it wherever your build needs more, following the data rule in [data/README.md](../README.md).
It's listed in [data/manifest.json](../manifest.json) as `fergie-seed`.

**Everything here is fictional.**
Fergie is loosely modeled on small Ontario towns like Fergus, New Dundee, Stratford, Shakespeare, Baden and St. Jacobs: a limestone downtown on a river, Scottish roots, a farmers' market, an antiques row and a summer theatre.
No real business, person, address or phone number is included. Don't add any.

The mix of people (ages, households, languages, housing, work) is weighted to match group-level **2021 Census** figures for a real small Ontario township.
Those figures are only proportions. No census record is in here, and Fergie isn't that township.
Source: [data/open/census_weights.json](../open/census_weights.json). Adapted from Statistics Canada, Census Profile, 2021 Census of Population.

---

## Meet Fergie

Fergie is a town of about 11,400 people on the Bannock River.
It has a stone downtown, a Saturday farmers' market, antique shops out at Bardsley Corners, the Riverside Players summer theatre, and a Highland Gathering every August.

See [town.json](town.json) for neighbourhoods, places, nearby towns and annual events.

---

## How it fits together

```
             town: neighbourhoods + places
                  │                │
        located in│                │held at
                  ▼                ▼
  business ◀── business_roles ── person ── rsvps ──▶ event
   │ owner text, deals,           │  │  │
   │ attributes, updates          │  │  └── memberships ──▶ group
   ◀──────────── follows ─────────┘  │
   ◀──────────── shoutouts ──────────┤
   │                                 └── writes ──▶ board post ──▶ replies ──▶ replies
   │ mentioned in                                      ▲ reactions
   ▼                                                   │
  news stories                       review_queue ◀── reports
  creators ── works                  notices (the town's own feed)
                                     activity.csv (tracked visits, some signed in)
```

**People never link to each other directly.** Nobody follows or friends a person.
Two residents are connected only through things they share: a group, a workplace, a thread, an event.

---

## Files

| File | What it contains | Count |
|---|---|---|
| [town.json](town.json) | Town profile: neighbourhoods, places (venues with addresses), nearby towns, annual events | 1 town, 16 places |
| [categories.json](categories.json) | Business categories | 12 |
| [businesses.json](businesses.json) | Businesses: hours, contact details, premises attributes, owner text, deals, claim status and where each fact came from | 93 |
| [business_roles.json](business_roles.json) | Who owns or works at which business | 91 |
| [users.json](users.json) | Accounts, including the three demo logins, with coarse optional profiles | 180 |
| [groups.json](groups.json) | Community groups, including the town's existing Facebook group | 15 |
| [memberships.json](memberships.json) | Who belongs to which group | 297 |
| [follows.json](follows.json) | Who follows which business, group, creator or news outlet | 800 |
| [events.json](events.json) | Past and upcoming events, some recurring | 54 |
| [rsvps.json](rsvps.json) | Who said they're going | 505 |
| [notices.json](notices.json) | The town's official notices: water main breaks, closures, outages | 41 |
| [board_posts.json](board_posts.json) | Community board posts: approved, pending and rejected | 221 |
| [replies.json](replies.json) | Threaded replies to board posts, at most two levels deep | 710 |
| [reactions.json](reactions.json) | Thanks, helpful and "me too" on posts, replies, shoutouts and updates | 1,064 |
| [business_updates.json](business_updates.json) | Short posts by verified owners | 47 |
| [shoutouts.json](shoutouts.json) | Positive recommendations of businesses (no star ratings) | 126 |
| [news.json](news.json) | Three local news outlets and their headlines | 32 stories |
| [creators.json](creators.json) | Local creators and their works | 20 creators, 86 works |
| [review_queue.json](review_queue.json) | Claims, edits, flags and other items waiting for an admin, plus past decisions | 47 |
| [reports.json](reports.json) | Who reported which reply, and why | 10 |
| [activity.csv](activity.csv) | 90 days of tracked site activity: searches, page views, contact clicks and shares | ~11,500 rows |

Websites use the reserved `.example` domain, emails use `example.com`, and phone numbers use the 555-0100 to 555-0199 range set aside for fiction.

---

## Demo accounts

`u_demo_admin`, `u_demo_resident` and `u_demo_owner` are the three demo accounts.
The demo business owner is the verified owner of Bannock Bakehouse.

---

## Schemas

**town.json**: the town's profile, including `timezone` (America/Toronto), `population_note`, `neighbourhoods` and `places`.
Each place has `id`, `name`, `kind` (`square`, `park`, `trail`, `hall`, `church`, `arena`, `site`, `school`, `landmark`), `landmark`, `description`, `address`, `geo`, `accessible` (`yes`, `limited`, `no`, `unknown`) and `capacity`.
Landmarks are the places with `landmark: true`. `neighbourhoods` include `rural`, for the countryside around town.

**businesses.json**: one object per business.

| Field | Notes |
|---|---|
| `id` | Slug, also used in URLs |
| `name`, `category`, `subcategory`, `description` | `category` matches an `id` in categories.json |
| `schema_type` | The schema.org type, e.g. `Bakery`, or a list like `["VeterinaryCare", "LocalBusiness"]` |
| `status` | `open` or `closed` |
| `address` | `street`, `neighbourhood`, `town`, `province`. Neighbourhoods are the same list people use. There's no postal code, so nobody invents a real-looking one |
| `geo` | `lat`, `lon`. Approximate and fictional, see known gaps |
| `phone`, `website`, `booking_url` | Any of these can be `null` |
| `social` | Links like `facebook` and `instagram`, or `null` |
| `hours` | `mon` to `sun`, each a list of `[open, close]` pairs in 24-hour time. An empty list means closed. A close time earlier than the open time means past midnight. `null` means unknown |
| `hours_note` | For example "By appointment" |
| `hours_exceptions` | Holiday closures and special hours: `date`, `closed`, `hours`, `note` |
| `seasonal` | `null`, or `open_from` and `open_to` as `MM-DD` |
| `price_level` | `$` to `$$$$`, or `null` |
| `cuisine` | Food places only, e.g. `["vietnamese"]` |
| `languages` | Languages spoken, e.g. `["en", "pa", "hi"]`. `pdc` is Pennsylvania German |
| `founded_year`, `history` | `history` is a list of `year` and `event` for a few older businesses |
| `area_served` | Trades and services that travel |
| `accepting_new_patients` | Health businesses only: `true`, `false` or `null` |
| `credentials` | Licences, all from a fictional registry |
| `payment` | Any of `cash`, `debit`, `credit`, `contactless`, `e-transfer`, `cheque` |
| `attributes` | Facts about the premises, OpenStreetMap-style. Every key is optional and missing means unknown. Keys include `wheelchair` (`yes`, `limited`, `no`, `unknown`) with `wheelchair_note`, `toilets_wheelchair`, `changing_table`, `level`, `parking`, `indoor_seating`, `outdoor_seating`, `takeaway`, `delivery`, `drive_through`, `reservation`, `internet_access`, `dog`, `smoking`, `air_conditioning`, `diet` (vegetarian, vegan, gluten-free and halal options), `kid_friendly`, `second_hand`, `organic`, plus `attributes_as_of` and `attributes_source` |
| `tags` | List |
| `owner_content` | Free text the verified owner writes about what they sell or do: `text`, `edited`, `edited_by`. `null` unless the claim is verified |
| `deals` | Each is only `text`, `url` and a time window (`starts`, `ends`) |
| `claim` | `status` is `unclaimed`, `pending` or `verified`, plus `owner_user_id` |
| `sources` | List of `fields`, `source` and `as_of`: which facts came from where, and when |
| `last_updated` | Date of the freshest fact |
| `data_note` | A short note about the listing, like an honour box or a seasonal move |

There are no menus, product lists or prices. What a business offers lives in `description`, `owner_content` and its `business_updates`, in its own words, the way a real small business keeps it.

**business_roles.json**: `user_id`, `business_id`, `role` (`owner`, `manager`, `staff`), `since`, `public` (whether the person chose to list the role on the business page).

**users.json**: `id`, `display_name`, `roles` (any of `resident`, `business_owner`, `staff`, `organiser`, `creator`, `reporter`, `admin`), `email`, `joined`, `bio`, `is_demo`, `account_status` (`active`, `suspended`, `erased`) and `profile`.
There are no passwords. Set up sign-in however you like, and keep secrets out of the repo.

`profile` is what each person told the portal about themselves when they signed up. Every field is optional, and many people leave some blank. People who live outside Fergie have no neighbourhood or years in town.
Personal details are deliberately coarse: an age band instead of a birthday, a neighbourhood instead of an address.

| Profile field | Values |
|---|---|
| `neighbourhood` | One of the town's neighbourhoods, or `null` |
| `age_band` | `18-24`, `25-34`, `35-44`, `45-54`, `55-64`, `65-74`, `75+` |
| `household_stage` | `single`, `couple`, `young_family`, `family_teens`, `empty_nest`, `multigenerational`, `shared` |
| `pets` | List of `dog`, `cat`, `other`, `none` |
| `years_in_town` | `under_1`, `1-5`, `6-20`, `20+`, `born_here` |
| `resident_type` | `year_round`, `seasonal`, `nearby`, `visitor` |
| `work_pattern` | `works_in_town`, `commutes`, `remote`, `retired`, `student`, `at_home` |
| `housing` | `own`, `rent` |
| `languages` | e.g. `["en", "fr"]` |
| `interests` | A few from a fixed list: `gardening`, `curling`, `theatre`, `antiques`, `hiking`, `kids_activities` and others |
| `gets_around` | `drives`, `no_car`, `cycles`, `prefers_walkable` |
| `access_filters` | Saved search filters like `step_free` or `accessible_toilet`. |
| `contact_preference`, `digest` | `email` or `none`; `daily`, `weekly` or `off` |

There's no gender, birthday, street address, phone, income or anything health-related on anyone. A town portal doesn't need them.

**groups.json**: `id`, `name`, `description`, `kind`, `verification` (`unverified`, `pending`, `verified`), `membership_policy` (`open`, `request`), `meets` (`schedule` and a `venue`), `website`, `external_url`.

**memberships.json**: `user_id`, `group_id`, `role` (`member`, `organiser`), `joined`, `status` (`active`, `requested`).

**follows.json**: `user_id`, `target_kind` (`business`, `group`, `creator`, `outlet`), `target_id`, `created`, `notify` (`instant`, `digest`, `none`).

**events.json**: `id`, `title`, `type`, `starts`, `ends` (with the Toronto time-zone offset), `venue` (`kind` is `place` or `business`, plus `id`), `location_text`, `organizer` (`kind` is `business`, `group` or `town`), `performers`, `description`, `tickets` (`name`, `price`, `currency`, `availability`), `is_free`, `capacity`, `age_range`, `attendance_mode` (`in_person`, `online`, `mixed`), `online_url`, `recurrence` (`freq`, `by_day` or `by_month_week`, `from`, `until`, `except`), `parent_event_id`, `rsvp_url` (for events that live on another site), `event_status` (`scheduled`, `cancelled`, `postponed`, `rescheduled`, `moved_online`), `previous_starts`, `moderation_status` (`approved`, `pending`, `rejected`) and `source`.

**rsvps.json**: `user_id`, `event_id`, `status` (`going`, `interested`, `cancelled`), `show_my_name`, `created`.

**notices.json**: `id`, `kind` (`water_main_break`, `road_closure`, `power_outage`, `boil_water`, `snow_clearing`, `tree_down`, `garbage_schedule`), `severity` (its scale depends on the kind: `minor`, `moderate` or `major` for water main breaks; `lane`, `partial` or `full` for road closures; `localized`, `block` or `multi-block` for outages; `advisory`; `routine` or `parking_ban`; `limb` or `full` for trees; `info`), `issued`, `expires`, `resolved`, `street`, `neighbourhood`, `text`, `source`.

**board_posts.json**: `id`, `author_user_id`, `posting_as` (a business or group, when an owner or organiser posts as them), `kind` (`lost_found`, `road_closure`, `looking_for`, `help_offered`, `event` or `general`), `title`, `body`, `neighbourhood`, `links` (to businesses, events, places or notices), `created`, `status` (`pending`, `approved` or `rejected`), `hold_reason` (why a pending post is waiting), `reviewed_by`, `rejection_reason`, `reply_count` and `reaction_counts`.

**replies.json**: `id`, `post_id`, `parent_reply_id`, `depth` (1 or 2), `author_user_id`, `posting_as`, `created`, `text`, `links`, `status` (`visible`, `hidden_pending_review`, `removed`, `deleted`) and `removal_reason`.

**reactions.json**: `user_id`, `target_kind` (`post`, `reply`, `shoutout`, `business_update`), `target_id`, `kind` (`thanks`, `helpful`, `me_too`), `created`. There are no dislikes. `me_too` only appears on "looking for" posts.

**business_updates.json**: `id`, `business_id`, `author_user_id`, `kind` (`announcement`, `new_in`, `hours_change`, `hiring`, `event`), `created`, `edited`, `expires`, `text`, `url`, `links`.

**shoutouts.json**: `id`, `author_user_id`, `business_id`, `status`, `text`, `created`. One per person per business, and never for your own business.

**news.json**: `outlets` (`id`, `name`, `kind`, `website`) and `stories` (`id`, `outlet_id`, `published`, `section`, `byline_user_id` or `byline`, `headline`, `summary`, `url`, `about`, `mentions`). Stories are headlines and short summaries that link out.

**creators.json**: `id`, `name`, `user_id`, `discipline`, `bio`, `website`, and `works`, each with `id`, `title`, `medium`, `series`, `year`, `dimensions`, `edition`, `licence`, `open_to_selling_prints`, `price_from`, `depicts_place_id`, `ownership` (`confirmed` or `pending`), `image` and `credit_line`.

**review_queue.json**: `id`, `kind` (`claim`, `edit`, `correction_flag`, `removal_request`, `event`, `creator_work` or `reported_reply`), `submitted_by`, `submitted`, `status`, `reviewed_by`, `details`. Depending on the kind, also `business_id`, `proposed` (the fields to change), `creator_id` and `work_id`, or, for reported replies, `reply_id`, `post_id`, `report_count`, `reasons`, `snapshot` (the text as reported), `outcome`, `public_reason` and `appeal`.

**reports.json**: `id`, `queue_id`, `target_kind`, `target_id`, `reporter_user_id`, `reason` (`spam`, `off_topic`, `unkind`, `personal_info`, `wrong_info`), `created`.

**activity.csv**

| Column | Notes |
|---|---|
| `timestamp` | Local time, ISO 8601 |
| `session_id` | One visit |
| `visitor_id` | The tracking cookie. The same browser keeps it across visits. Blank unless the visitor accepted cookies |
| `user_id` | The resident's account, when they were signed in. Otherwise blank |
| `consent` | What the visitor chose on the cookie banner: `accepted`, `declined` or `not_answered` |
| `event` | `search`, `page_view`, `contact_click` or `share` |
| `query`, `results_count` | For searches |
| `business_id` | For page views, contact clicks and shares |
| `action` | For contact clicks: `website`, `call`, `directions` or `booking`. For shares: `copy_link`, `facebook`, `text_message` or `email` |
| `visitor_region` | Coarse only: `fergie`, `nearby`, `elsewhere` or `unknown` |
| `device` | `mobile` or `desktop` |
| `referrer` | `direct`, `search_engine`, `ai_assistant`, `social` or `qr` |

---

## Known gaps

- **Dates are fixed.** The seed's "today" is 2026-11-20 (`town.seed_anchor_date`). Posts and activity run up to that date, notices go back to December 2025, and events run into 2027. Shift them if your demo needs to look current.
- **The map won't line up.** Coordinates sit near a real Ontario town, so a real basemap shows real streets under Fergie's made-up ones. For a map module, consider drawing Fergie's own map.
- **No images.** Creators' works and businesses have no pictures. Use placeholders, or make your own. For real art to build galleries and prints on, [data/open/met_works.json](../open/met_works.json) has ten public-domain works from The Met, credited to their real makers. They aren't by Fergie's creators, so don't attach them to one.
- **No out-of-town businesses.** Nearby places are named in `town.json`, but there are no listings for them.
- **English only**, though profiles and businesses record other languages spoken.
- **The text is template-made.** Posts and replies come from banks of phrases, so they repeat more than real people would.
- **Activity is simulated.** Real traffic would be messier.

---

## Extending

The seed files are provided as-is, and the checker compares them against their checksums.
The script that generates them stays with the track, because it would give away what the judging walkthrough looks for.

Don't edit these files by hand.
To add to Fergie or change it, for example to shift the dates, write your own script that reads these files and writes the result to a folder of your own, then list it in the manifest. [data/README.md](../README.md) shows how.

Before it was written, the seed was checked so that:
- every reference points to something that exists
- replies come after their posts, and nobody acts before they joined
- nobody reacts to their own content or follows a person
- no personal fields are present, and phones, emails and websites stay in the reserved fictional ranges
