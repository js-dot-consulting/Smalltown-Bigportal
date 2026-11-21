# Requirements

This file covers what every team builds and what you can skip.
Everything else is your call.

The core is sized so a team of three can build it well in a weekend, with time left for the part you care about.

---

## To be judged at all

These are pass or fail. See "Eligibility" in [JUDGING.md](JUDGING.md).

- A front end and a back end, with real data flowing between them
- Live at a public URL for the whole judging period
- A login page with one-click demo logins for **demo admin**, **demo resident** and **demo business owner**
- `submission/SUBMISSION.md` filled in
- No secrets, API keys or real personal data in the repo
- A demo video that meets the event's rules, showing your live site running
- A public repo by the deadline
- A demo that runs on the Fergie seed data in `data/seed/`

---

## Data

Your demo runs on the Fergie seed data. Add to it wherever your build needs more.

Every dataset in the repo, ours and yours, is listed in `data/manifest.json` with its source, license and the script that made it.
**AI can write the script that gets the data. It can't write the data.**
Where the seed stops, look for open data that already exists before you make anything up.

[data/README.md](data/README.md) explains the rule, the manifest and the checker.
Data the checker can't trace gets flagged in judging. See "Data checks" in [JUDGING.md](JUDGING.md).

---

## Roles

| Role | Who they are | What they can do |
|---|---|---|
| Visitor | Anyone, no account | Search and read everything public, and contact businesses |
| Resident | Anyone who signs up | Everything a visitor can do, plus post to the community board, claim a business and flag mistakes |
| Business owner | A resident who has claimed a business | Suggest edits to that business. Once an admin verifies them, their edits to **their own business** go live without review |
| Admin | Runs the site | Work the review queue, verify business owners, and edit or remove anything |

A business owner can own more than one business.
Verification covers only the businesses they've been verified for.
Their board posts and anything else they submit still go through review.

The **demo business owner** login should be a verified owner of at least one business, so a judge can see an edit go live.

---

## Core features

Every team builds these.
They're scored under "A1. Core features" in [JUDGING.md](JUDGING.md).

Each one has a minimum bar.
Meeting it solidly, with real data flowing through it, is what a 7 looks like.
These are minimums, not a spec. Meet them however you like, and go further where it matters to you.

| # | Feature | Minimum bar |
|---|---|---|
| C1 | **Logins and roles** | Residents can sign up and sign in. Every role's permissions are checked on the server, not only hidden in the interface. |
| C2 | **Business directory** | A visitor without an account can search by name, browse by category, and open a business page showing what the business does, where it is, when it's open and how to reach it. Every page links out to the business's own site, phone or booking where those exist. |
| C3 | **Claimable business pages** | A resident can claim a business. An admin can verify the claim. A verified owner can edit their own business, and the change goes live right away. Each fact shows where it came from and how fresh it is. |
| C4 | **Community board** | Signed-in residents can post to the town, like a lost dog, a road closure or a general message. Approved posts are public, and each post is easy to share, with a link that previews well on social media and in messaging apps. |
| C5 | **Admin review queue** | Board posts, business claims and edits from anyone who isn't a verified owner wait in a queue until an admin approves or rejects them. Nothing skips it except a verified owner's edits to their own business. Admin pages and actions are refused to everyone without the admin role. |

---

## Tracking

Like any platform, the portal tracks what visitors and residents do, signed in or not.
It uses what it learns to make recommendations, and to give businesses insights about their traffic and leads.

The default we're setting is a small, accept-all style cookie banner on a visitor's first visit, with a rolling six-month consent.
You can change it if you have a better idea. Tell us why.
How it looks and works is up to you.

## What businesses can pay for

Claiming a business page is free.
Businesses can pay for more: deeper analytics on the leads that reach them, and extra details and decoration on their own page.
Paying never puts one business in place of another's listing.

---

## Beyond the core

Build **at least one module** beyond the core features.
Judges score each module you list for depth, then take the average, so one or two deep modules beat many shallow ones.

[docs/project-directions.md](docs/project-directions.md) has starting points, and original ideas are welcome.
The bonus bounties in [JUDGING.md](JUDGING.md) are another place to look.

Wherever it fits, make things easy to share.
Business pages, events, deals and creators' work should travel well to wherever residents already talk, and bring people back to the town's own site.

---

## Out of scope

Don't spend your time on these.
Build as if the assumption on the right is already true.

| Out of scope | Assume instead |
|---|---|
| Checking that a poster lives in the town | Anyone can make an account. Human review handles bad actors. |
| Checking that a business owner is real | Verification happens offline. An admin flips a "verified" switch. |
| A checkout or store inside the platform | Print-on-demand services handle checkout, printing and shipping. |
| Real payments and payouts | Track what's owed and show it clearly. Nobody needs to be paid for real. |
| Sending email | Show the message on screen, or log it, instead of sending it. |
| Password reset and account recovery | Simple sign-up and the demo logins are enough. |
| Native mobile apps | A website that works well on a phone is enough. |
| Live updates | Refreshing the page to see new content is fine. |
| Crawling or scraping businesses' websites | Fergie's businesses are fictional, so there's nothing real to crawl. Work from the seed data and open datasets, and don't send automated traffic to real local businesses. |

Shortcuts are welcome.
Ready-made login services, hosted databases, starter templates and simple pre-made demo accounts are all fine.
Tell us what you used and why.

---

## Event rules

The event's own rules apply to every track and take priority over this repo.
They're published by the organizers.
We don't copy dates, deadlines or event logistics here, so nothing in this repo goes stale.

---

## Open to you

Anything not listed above is your call:

- Stack, frameworks and hosting
- Tools and services
- Design and branding
- Which project directions to pursue, or an idea of your own

Building your own or using something that already exists are both fine.
Tell us why you chose what you did.
