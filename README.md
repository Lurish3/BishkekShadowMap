# Bishkek Comfort Map

Bishkek Comfort Map is a GIS prototype for finding and analyzing comfortable pedestrian routes in Bishkek. Route selection accounts for distance and travel time, shade, greenery, sidewalks, crossings, safety, and changing conditions throughout the day.

## Project Goal

The project demonstrates comfort-aware pedestrian routing and shows several meaningful alternatives instead of selecting a route based only on the shortest distance.

## What the Product Shows

- alternative routes such as fastest, shadiest, and most comfortable;
- dynamic route changes based on date and time;
- map layers for solar exposure, greenery, pedestrian infrastructure, and comfort;
- comparisons by time, distance, shade, greenery, and safety;
- adjustable weights for sun exposure, greenery, sidewalks, stairs, and speed;
- route recalculation when parameters change.

## Technology Stack

- Python
- GeoPandas, Shapely, OSMnx, NetworkX
- NumPy and Pandas
- PostgreSQL / PostGIS
- FastAPI
- Leaflet / MapLibre

## Architecture

```text
BishkekShadowMap/
├── README.md
├── requirements.txt
├── .gitignore
├── app/
│   ├── main.py
│   └── README.md
├── src/
│   ├── __init__.py
│   ├── solar/
│   │   ├── __init__.py
│   │   └── sun_model.py
│   ├── routing/
│   │   ├── __init__.py
│   │   ├── graph.py
│   │   └── route_optimizer.py
│   ├── greenery/
│   │   └── __init__.py
│   └── comfort/
│       ├── __init__.py
│       └── comfort_model.py
├── data/
│   ├── raw/
│   │   └── README.md
│   └── processed/
│       └── README.md
├── research/
│   ├── methodology/
│   │   └── README.md
│   ├── questionnaire/
│   │   └── README.md
│   └── analysis/
│       └── README.md
├── results/
│   └── README.md
├── tests/
│   └── test_route_logic.py
└── docs/
    └── architecture.md
```

## Route Model

A road-network node contains an identifier, coordinates, elevation, and surrounding-environment properties. An edge includes distance, walking time, sun exposure, shade ratio, greenery, sidewalk quality, stairs, crossings, transport access, and time-dependent conditions.

The objective function is:

`Cost = w_time * t + w_sun * sun_exposure + w_sidewalk * penalty + w_stairs * penalty - w_greenery * greenery`

This supports multi-objective routing and Pareto-optimal alternatives.

## Local Setup

```bash
git clone https://github.com/Lurish3/BishkekShadowMap.git
cd BishkekShadowMap
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open the API documentation at <http://127.0.0.1:8000/docs>.

## Roadmap

- **0.1:** basic A→B route, graph, solar model, time slider, and alternatives;
- **0.2:** route weights, Pareto optimization, layers, explanations, and comparison;
- **0.3:** What-if scenarios, Simulate Walk, School Mode, transport, and analytics;
- **Later:** validation with real-world data and evaluation of the model.

## Risks and Limitations

The solar model is an estimate rather than a physical measurement. Accuracy depends on the quality and freshness of the source geodata. The project is not intended to provide real-time navigation.

## License

MIT

Author: Lurish3

Repository: https://github.com/Lurish3/BishkekShadowMap
