# How to Make a LinkedIn Announcement (PDF + Post Text)

As of 2026-11-08. Based on the Nov 12, 2026 announcement session.

## Overview

A meeting announcement is two pieces: a PDF of one square image per talk, and a plain-text post that carries the full details.

This guide comes from the Nov 12, 2026 announcement (Yun Chang and Husan Mavlonov), which took six rounds of revisions before the design was right.

The workflow that finally worked:

1. Gather facts from the repo: `content/calendar.yaml` and the talk's news file (e.g. `content/news/25-yun-chang-talk-announcement.md`), plus photos from `images/news/` and `images/robot-logo.png`.
2. Design one image as HTML, render it to JPEG, and get approval before starting the second.
3. Build the second image from the first one's source so the two match.
4. Combine the approved JPEGs into a PDF.
5. Write the post text in Pito's voice, with full titles and details.

## Creating the PDF

Make each page as a separate square JPEG, approve it, then merge. **Never iterate on the PDF directly.**

### Content per page

One talk per page, plus when and where. Nothing else: no agenda, no talk summary, no second talk.

- **Top row:** logo and "Boston Robot Hackers" on the left; a red date tag on the right ("THU NOV 12 · 7PM").
- **Kicker:** "Featured talk" or "Short talk" in amber.
- **Headline:** the talk title in very large condensed capitals, split into a short headline and a subtitle if it's long.
- **Speaker:** name large, a short role beside it ("MIT PhD · SPARK Lab", "CEO · Defex Robotics").
- **Bottom bar:** venue on the left ("Artisans Asylum · Allston"), `brh.eventbrite.com` on the right.

### Design that was approved

| Element | Value |
| --- | --- |
| Size | 1080×1080 px, square |
| Background | near-black `#07080c`; bar `#0e1017` with a 4px red top border |
| Accent colors | red `#d00029` (date tag), amber `#ffb020` (kicker, URL) |
| Fonts | Avenir Next Condensed 700–800 for headline and labels; Avenir Next for body |
| Headline | 104–112 px, line-height 0.92, uppercase |
| Smallest text | about 38 px |
| Photo | full-bleed at the top, fading into black where the text starts |
| Cut-out photo | on the right, lit by a soft radial glow in a color taken from the object |
| Logo | on a white disc, since the black line art vanishes on dark |

### Build steps

1. Copy the photos and logo into a `src/` folder in the scratchpad. Write the page as HTML sized exactly to 1080×1080.

2. Render with headless Chrome. Include `--virtual-time-budget=3000`, or images may not load before the screenshot:

    ```bash
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
      --hide-scrollbars --force-device-scale-factor=1 --virtual-time-budget=3000 \
      --window-size=1080,1080 --screenshot=preview/yun.png file://$PWD/src/yun.html
    sips -s format jpeg -s formatOptions 92 preview/yun.png --out linkedin/1-yun-chang.jpg
    ```

3. Check legibility on a copy shrunk to phone-feed width: `sips -Z 360 1-yun-chang.jpg --out preview/small.jpg`.

4. Merge the approved JPEGs without recompressing them:

    ```bash
    uv run --with img2pdf python -c "import img2pdf; open('brh-nov12-talks.pdf','wb').write(img2pdf.convert(['1-yun-chang.jpg','2-husan-mavlonov.jpg']))"
    ```

The result was two square pages, about 490 KB. Order the pages to match the post, featured talk first.

## Writing the post text

The post carries what the images leave out: full titles, exact times, the full address, and a blurb for each talk. Write it with the `pito-voice` skill.

### Structure, in order

1. **Opening:** start with "I am excited to announce our next Boston Robot Hackers meeting, this Thursday, November 12." Follow with one sentence that makes the two talks concrete ("one about robots the size of a Bobcat loader, and one about robots that plug in connectors").
2. **Logistics block:** three plain lines.
    - When: Thursday, November 12, 7:00 to 9:00pm
    - Where: Artisans Asylum, 96 Holton Street, Boston (Allston)
    - Register: https://brh.eventbrite.com
3. **Featured talk:** a header line with time, full title and speaker, then one paragraph: the question the talk answers, what it covers, and the speaker's background.
4. **Short talk:** the same shape, in one shorter paragraph.
5. **Closing:** "As always, we start at 7:00 with mingling and show and tell. Bring something you're building."

### Rules

- **Plain text only:** LinkedIn posts don't render markdown bold, so no `**`.
- **Full talk titles:** the images can shorten titles; the post should not.
- **Blurbs from the source:** condense the abstract and bio in the news file. Don't invent claims.
- **Consistent order:** last time the featured talk (7:50pm) was listed before the short talk (7:30pm), with times shown on each.

## Pitfalls from last time

Most of the wasted rounds came from starting with a crowded, generic layout and patching it. Starting over with a bold design fixed it in one pass.

| What went wrong | Do this instead |
| --- | --- |
| First draft packed both talks, an agenda and summaries onto two pages | One talk per page, plus date, time and place |
| Images squeezed into strips, letterboxed on black, or floating unattached | Full-bleed photo fading into the text, or a cut-out object with a glow |
| A white card layout read as "ugly" | Dark background, large condensed type, strong accent colors |
| Iterating directly on the PDF | Approve one JPEG at a time, then merge |
| 4:5 portrait (1080×1350) | Square 1080×1080 was preferred |
| Preview and intermediate files left in the folder the user was watching | Keep only approval JPEGs there; put previews in a separate `preview/` folder |
| Logo missing from the render | Add `--virtual-time-budget=3000`; put dark line art on a white disc |
| "Free" added without a source | Only state facts found in the repo |
| Shortened titles and condensed roles not flagged | Tell the user every wording change from the source |
| Scratchpad deleted at session end | Copy the final PDF somewhere permanent before uploading |

## Pre-publish checklist

- [ ] Date, time and venue match `content/calendar.yaml`
- [ ] Each image is 1080×1080 and readable at 360 px wide
- [ ] Logo is visible on each image
- [ ] Both images share the same top row, date tag, type and bottom bar
- [ ] PDF pages are in the right order, about 0.5 MB
- [ ] Post has the opening line, logistics block, both blurbs and the Eventbrite link
- [ ] Post uses full titles and has no markdown formatting
- [ ] Every shortened title or condensed role has been approved
- [ ] Final PDF is copied out of the scratchpad
