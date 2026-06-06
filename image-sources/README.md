# Swappable site images

These 10 images are decorative thumbnails shown on news/meeting cards. They are
displayed in a **small square box** (cards: 80×80, homepage: 1:1) with
`object-fit: cover`, so **source images should be square** (1024×1024 works well).

Two interchangeable sets live here:

| Folder | What |
|--------|------|
| `handdrawn/` | Original pencil / woodcut sketches |
| `photo/` | Photographic versions |

`images/` (the live folder the build ships) holds whichever set is currently active.
This `image-sources/` folder is **not** copied into `output/`.

## Revert to the hand-drawn sketches

```bash
scripts/set-images.sh handdrawn
uv run python build/build.py
```

## Use the photos

```bash
scripts/set-images.sh photo
uv run python build/build.py
```

## Provide a better image

Drop a **square** PNG into `image-sources/photo/` with the same filename
(e.g. `talk.png`), then:

```bash
scripts/set-images.sh photo
uv run python build/build.py
```

## The files

`armwork` `battery` `clock` `kalman2` `leo-1` `meeting-2` `meeting-3`
`neuraltraining` `talk` `workbench`

(Note: `kalman.png` is a sketch that no content references, so it is not part of
either set.)
