# Guide template

Copy this into `_guides/<slug>.md` and fill it in. The slug becomes the URL:
`_guides/word-copilot-tab-missing.md` → `https://navisualguide.com/guides/word-copilot-tab-missing/`

Excluded from the built site (see `exclude:` in `_config.yml`), so it is safe to leave here.

**Choose the slug carefully — the URL is expensive to change later** (changing it means a redirect
and lost link equity). Prefer the words a person would actually search.

---

```markdown
---
title: "The Copilot tab isn't in your Word Options — how to actually remove it"
description: "Most guides say Options ▸ Copilot, or a Word menu. Neither exists in current Windows builds. Here's what's actually on your screen, version by version."
date: 2026-09-02
# last_modified: 2026-10-01   # add when you meaningfully revise; drives sitemap lastmod
app: "Microsoft Word"
os: "Windows 11"

# `steps:` is OPTIONAL but it is the point of the exercise — supplying it makes the
# layout emit HowTo structured data instead of plain TechArticle, which is what lets
# an AI answer engine cite this as a procedure rather than prose.
#
# Keep these in sync with the numbered steps in the body. They are written twice on
# purpose: scraping steps back out of rendered prose is fragile, and structured data
# that silently drifts from the visible page is a penalty risk.
steps:
  - name: "Open File ▸ Options"
    text: "From any open document, choose File, then Options at the bottom of the left rail."
  - name: "Go to Trust Center ▸ Trust Center Settings"
    text: "The Copilot controls are not on a Copilot tab in this build; they live under Trust Center."
  - name: "Turn off connected experiences"
    text: "Clear the checkbox for optional connected experiences, then click OK."
---

One or two sentences naming the symptom in the reader's own words, and — this part
matters — **naming the wrong advice explicitly**. "Most guides tell you to open
Options ▸ Copilot; that tab doesn't exist in your build." That mismatch *is* the
search intent, so say it out loud rather than burying it.

## Before you start

Which versions this applies to, and how the reader checks which one they have.

## Steps

1. **Open File ▸ Options.** What you should see when it works.
2. **Go to Trust Center ▸ Trust Center Settings.** Note here if this is the step
   that commonly fails silently — that is the highest-value sentence on the page.
3. **Turn off connected experiences.** Confirm what changes on screen afterwards.

## If step 2 looked different

The variant paths, by version/tenant/edition.

**This section is the moat.** It is the part a generic answer cannot do, because it
does not know which build is in front of this particular reader. Everything above
this heading is commodity; this is why the page deserves to exist.

## Why this is hard to find

Optional, short. Good place for the honest structural observation — that the setting
is three dialogs deep, or moved between versions.
```

---

## Rules worth keeping

- **Numbered steps in the body must match `steps:` in the front matter.** They generate the
  HowTo schema; drift between them is a real penalty risk, not a cosmetic issue.
- **One idea per guide.** Ultra-specific beats broad on a zero-authority domain — see
  `marketing-plan.md` D1c: do not chase "how to make a pivot table in Excel."
- **Only write about apps we can actually point at.** If the locator gets nothing (SolidWorks:
  zero UIA descendants), a screenshot showing a miss is worse than no article.
- **Do not add `aggregateRating`.** No real reviews exist; inventing them is a known Google
  structured-data penalty and is dishonest besides.
