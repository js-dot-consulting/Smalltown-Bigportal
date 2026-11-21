# Smalltown Bigportal

> Give a small town its own front door to the internet.

**Sponsor:** James Strang
**Event:** K-Dub Hacks 2026

Dates, deadlines and event logistics live with the event organizers, not in this repo, so they're never out of date here.

---

## The problem

Ask how things work in a small town and you hear "check the Facebook group."
That's where people go to find a plumber, see what's on this weekend, or ask whose dog is loose on Main Street.

That means the town's front door to the internet belongs to someone else.

- **Residents** dig through feeds built to keep them scrolling, not to get them an answer.
- **Local businesses** pay to reach neighbours who already follow them, or get buried by the algorithm.
  Many have no website, or one nobody has touched in years.
- **Visitors and AI assistants** can't tell what's open, what's good or what exists.
  They end up sending people to the bigger town down the highway.
- **Local news and community groups** do the work of keeping the town informed, while the platform keeps the audience.
- **Nobody in town** can see what people are looking for and can't find.
  That's exactly what someone thinking of opening a business needs to know.

The big platforms are very good at one thing.
They watch what people do, learn what they want, and turn that into money.
That flywheel works. It just isn't pointed at the town.

**What would it look like to build that flywheel for a town, pointed at its own businesses, groups and news, without harming the people it's meant to serve?**

## Why now

More and more people find things by asking an AI assistant instead of scrolling or searching.
An assistant can only recommend what it can read and trust.
A town that publishes clean, accurate, up-to-date facts about itself gets found.
A town that doesn't gets left out.

## What you're building

A web portal for one small town, on the town's own domain, that any town could run.

It should help a resident who never makes an account and send visitors straight to local businesses.
It should give the town signals about itself that until now only a platform could see.

You'll build for **Fergie**, a fictional small Ontario town with seed data ready to go, so you can start building on the first morning.
Build it so any other town could swap in its own name and data.

## What success looks like

Judge a visit by what it does for the town, not by how long it lasts. A good visit:

- gets someone something useful
- gives them a reason to come back, or to share the site
- sends money to local businesses and people

How well a portal does over years depends on how a real town takes it up, and nobody can predict that.
What you can show is that the visits that do happen do these things.

## Who it's for

| Who | What they need |
|---|---|
| Residents | Answers without an account: who does this, is it open, what's happening |
| Visitors and AI assistants | Accurate pages that lead straight to the business |
| Business owners | A way to be found and keep their facts right, without paying a platform for reach |
| Local news, groups and creators | More attention and traffic, not competition |
| The town or BIA | Group-level signals about what the town is missing, and a way to act on them |

## Where the interesting problems are

There's a core that every team builds, described in [REQUIREMENTS.md](REQUIREMENTS.md).
After that, the questions are yours. Here are a few we find hard:

- How do you help someone who will never sign up?
- How do you learn from everyone who uses the site, and still be trusted by them?
- How do you make money for the town without standing between a customer and a shop?
- How do you reach the neighbour who will never open an app?
- How do you make sure a business's page tells the truth, and stays true after you stop looking?

You don't have to rebuild Facebook, and you don't have to build everything.
Build something a real town could switch on, and go deep on the part you believe in.
Original ideas are welcome and score well.

The must-haves are in [REQUIREMENTS.md](REQUIREMENTS.md).
The values we judge against are in [PRINCIPLES.md](PRINCIPLES.md).
How we score is in [JUDGING.md](JUDGING.md).

Everything beyond that is yours to decide.

## Getting started

1. Fork this repo.
   If you want your work private during the event, use **Use this template** instead. GitHub forks of a public repo stay public.
   Either way, your repo must be public by the deadline.
2. Read this file, then `PRINCIPLES.md`, `REQUIREMENTS.md` and `JUDGING.md`.
3. Open `AGENTS.md` with your team and your AI tools.
   Have the conversation it asks for before you build.
4. Skim `docs/` and `data/` for project directions, resources, common questions and starting data.
5. Build. Experiment anywhere in the repo.
6. Put what you want judged in `submission/`.
7. Deploy it to a live URL.
8. Record a demo video of the live site.

## How submissions work

- Your project must be live at a public URL for the whole judging period.
- You also need a demo video of the live site that meets the event's rules. The video doesn't replace the live URL. We need both.
- Your repo must be public by the deadline.
- Your login page must have one-click demo logins for three roles: **demo admin**, **demo resident** and **demo business owner**.
- Your demo runs on the Fergie seed data, and every dataset is listed in `data/manifest.json`. See [data/README.md](data/README.md).
- Automated checks, most of them AI-based, pick a shortlist of six, and a judge picks the winners from it. Trying to manipulate the judging, human or automated, disqualifies the team. See [JUDGING.md](JUDGING.md).
- Judging starts in `submission/`. We look there first.
- You can create any other folders or files in the repo while you work.
- Your submission may reference code and files outside `submission/`.
  Link to them from `submission/SUBMISSION.md` so judges can find them.
- Fill in `submission/SUBMISSION.md` before the deadline.

The deadline and how to submit are set by the event organizers. Check the event's official information.

## Using AI

We expect you to use AI heavily, and that's fine.

Everything in this repo is written for your team and your AI to read together.
You make the decisions. Your AI helps you build them.

Tell us in `SUBMISSION.md` where AI helped and where you overruled it.

## Repo map

```
.
├── README.md            The problem and how this track works
├── AGENTS.md            Starter file for your AI tools (yours to rewrite)
├── CLAUDE.md            Points Claude-based tools at AGENTS.md
├── PRINCIPLES.md        The values we judge against
├── REQUIREMENTS.md      Must-haves and out of scope
├── JUDGING.md           Rubric and bonus bounties
├── LICENSE              The Unlicense: no restrictions on use
├── docs/
│   ├── project-directions.md   Non-exhaustive starting points
│   ├── resources.md            Data sources, APIs, tools, licensing notes
│   └── faq.md                  Common questions
├── data/
│   ├── README.md               The data rule, the manifest and the checker
│   ├── manifest.json           Every dataset, its source, license and script
│   ├── check_data.py           Checks the manifest against what's in the repo
│   ├── seed/                   The fictional town of Fergie. Your demo runs on this
│   └── open/                   Real, openly licensed data that fills gaps in the seed
└── submission/
    ├── SUBMISSION.md           Fill this in. Judging starts here.
    └── LICENSE                 Default license for everything your team adds
```

## Help during the event

Check [docs/faq.md](docs/faq.md) first.
For anything else, use the contact channels the event organizers give you.

## License

Track materials are released under [The Unlicense](LICENSE). There are no restrictions on use.

Your team owns the work you build.
Everything you add to this repo is licensed by default under [MIT No Attribution](submission/LICENSE).
That lets the sponsor and anyone else use, change and share it for any purpose.
The event's own terms and the sponsor terms also apply. See [docs/faq.md](docs/faq.md).
