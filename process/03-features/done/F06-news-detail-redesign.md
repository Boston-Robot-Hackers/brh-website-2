# F06 — News detail page: two consistent redesign options
**Priority**: Medium
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes

**Description**:
* The current news detail page (`templates/details/news-detail.html`) was
  restyled in F05/TF05.9 to reuse the shared `.detail-header*`/
  `.detail-page` system — functional and on-theme, but generic (shared
  verbatim with meeting-detail's shape: photo + title + date + excerpt,
  then raw markdown, then a back button), not tailored to what a single
  news article specifically wants.
* This feature is exploration only, matching F04's pattern: research a
  couple of real examples of how editorial/news sites present a single
  article (building on the same real-world reference research already
  done for Option D — futurism.com — plus 1-2 more), then produce **two**
  concrete redesign options for the news-detail page, staying consistent
  with the site's already-established Option D theme (Archivo Narrow,
  cream/ink/red palette, existing nav/footer chrome) rather than
  introducing a new unrelated look.
* Both options are standalone mockups (`design-mockups/f06-news-detail-redesign/`,
  same convention as F04) built against one real, already-published news
  post's real content — not invented copy, not wired into the real
  `templates/details/news-detail.html` yet.
* Continues on the existing `f04-site-redesign` branch (already has this
  entire redesign's lineage and is unmerged).

**Non-goals**:
* Implementing either option into the real site — deferred to a follow-up
  feature once the user picks a direction.
* Redesigning meeting/project/member detail pages (out of scope here,
  though a future feature might extend whichever direction is chosen).
* Inventing new news content — both options reuse one real existing post.

## How to Demo
**Setup**: None — standalone HTML mockups, no build step required.

**Steps**:
1. Open both mockup files (or the published comparison artifact).
2. Compare the two article-page treatments against the same real post.
3. Confirm both stay visually consistent with the rest of the site
   (palette, type, nav/footer) while differing from each other and from
   the current generic detail-page shape.

**Expected output**: Two clearly differentiated, on-theme news-article
page designs to choose from, with zero changes to the live
`templates/`/`build/` pipeline.

## Process Gate
After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
