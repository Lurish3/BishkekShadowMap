# Bishkek Comfort Map

Bishkek Comfort Map is a GIS prototype for finding and analyzing comfortable pedestrian routes in Bishkek. Route selection accounts for distance and travel time, shade, greenery, sidewalks, crossings, and route trade-offs.

## Local setup

The pinned scientific dependencies are intended for Python 3.12 or 3.13. On Arch Linux, Python 3.12 may be installed through `uv`; this avoids installing packages into the system-managed Python environment.

### Fish shell / Arch Linux

```fish
sudo pacman -Syu
sudo pacman -S --needed uv
cd BishkekShadowMap
rm -rf .venv
uv python install 3.12
uv venv --python 3.12 .venv
source .venv/bin/activate.fish
uv pip install --python .venv/bin/python -r requirements.txt
uv run --python .venv/bin/python uvicorn app.main:app --reload
```

### Bash / macOS / Linux

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install --only-binary=:all: -r requirements.txt
uvicorn app.main:app --reload
```

Run the tests with:

```bash
python -m pytest -q
```

Open the API documentation at <http://127.0.0.1:8000/docs>.

## API

- `GET /` — service metadata
- `GET /health` — health check
- `POST /routes` — validated route alternatives

`POST /routes` accepts ISO date/time values and non-negative weights from 0 to 10. Invalid values receive a `422` response instead of reaching the route model.
