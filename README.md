# Floor Plan Analyzer

Analyzes floor plan images: detects rooms, labels them, and exports room segments as JSON.

Room segmentation works by treating walls and other barriers as obstacles and flood-filling the remaining free space: each connected region of free pixels becomes a candidate room. Regions smaller than a configurable minimum area are discarded as noise. For each detected room the app computes its centroid and boundary segments (contour), which are used both for the visual overlay and the exported JSON data.

# Limitations
- amount of images

# Assumptions
- above part of the walls can be used as breakers for the entire plan
- parts, that are between the walls and background are balkon or something on the outside

# Next steps

1. Improve image preprocessing to better distinguish the upper edges of walls from other objects in the image.
2. Add filtering for the final components/segments in the image.
3. Test SAM on existing images if quality is more important than speed.

## Requirements

- Python 3.12+
- [Poetry](https://python-poetry.org/docs/#installation)

## Local setup

```bash
poetry install --no-root
PYTHONPATH=. poetry run streamlit run src/app.py
```

Open http://localhost:8501

## Docker

```bash
docker compose up --build
```

Open http://localhost:8501

To run in the background:

```bash
docker compose up --build -d
docker compose logs -f
```

Stop:

```bash
docker compose down
```

## Usage

1. Upload a floor plan image (`png`, `jpg`, `jpeg`, `webp`).
2. Adjust processing parameters if needed (background removal, thresholds, minimum room area, overlay opacity).
3. View the detected and labeled rooms.
4. Download room data as `rooms.json`.
