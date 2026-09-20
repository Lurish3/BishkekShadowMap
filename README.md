# Bishkek Comfort Map

Bishkek Comfort Map is a GIS prototype for finding and analyzing comfortable pedestrian routes in Bishkek. The project demonstrates how route choice can account not only for distance and travel time, but also for shade, greenery, sidewalks, crossings, safety, and changing conditions throughout the day.

## Why This Matters

Bishkek residents face a common set of problems:

1. Routes are built without properly accounting for the pedestrian network and often pass through inconvenient areas.
2. The same origin and destination may produce the same route at different times of day, even though conditions change.
3. Data is often static and does not reflect actual shade, greenery, or crossing availability.
4. A route may pass through unsafe or uncomfortable areas, such as roads, poor-quality surfaces, or narrow passages.
5. Users cannot quickly select route preferences or recalculate routes under different conditions.

This project treats route selection not as a simple “find the shortest path” problem, but as a multi-criteria optimization problem. The goal is to show several meaningful alternatives and explain the trade-offs between them.

## Project Goal

To demonstrate how comfort-aware routing can provide additional value to pedestrians in Bishkek compared with conventional routing based primarily on distance or speed.

## Audience

- Bishkek residents;
- people who walk around the city;
- students, schoolchildren, workers, and anyone who chooses routes based on comfort rather than speed alone;
- researchers studying urban mobility and public space.

## What the Product Shows

- three or more alternative routes: fastest, shadiest, and most comfortable;
- dynamic route changes based on the time of day and date;
- map layers for Solar Exposure, Greenery, Pedestrian Infrastructure, and Comfort;
- route explanations such as “+3 minutes, but −42% solar exposure and +18% sidewalk coverage”;
- comparisons of alternatives by time, distance, shade, greenery, and safety;
- adjustable weights for sun exposure, greenery, sidewalks, stairs, and speed;
- route recalculation when parameters or the time window change.

## MVP 0.1

The minimum working prototype includes:

- a small area of Bishkek;
- an A→B route;
- a pedestrian graph;
- a basic solar model;
- a time slider;
- 2–3 alternative routes;
- key metrics: time, distance, shade percentage, greenery, and route explanations.

## Development Plan

### MVP 0.2

- route weights and recalculation based on user preferences;
- Pareto optimization and route alternatives;
- urban context layers;
- scenario comparison and route-choice explanations.

### MVP 0.3

- What-if scenarios such as “add a tree” or “add a crossing”;
- Simulate Walk — visualization of movement along a route over time;
- School Mode;
- transport and urban analysis;
- extended analytics for the urban environment.

## Technology Stack

- Python
- GeoPandas
- Shapely
- OSMnx
- NetworkX
- NumPy
- Pandas
- PostgreSQL / PostGIS
- FastAPI
- Leaflet / MapLibre
- React / TypeScript, if needed

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
│       ��── __init__.py
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

A road-network node contains:

- an identifier;
- coordinates;
- elevation;
- surrounding-environment properties.

An edge between nodes includes:

- `distance`;
- `walking_time`;
- `sun_exposure`;
- `shade_ratio`;
- `greenery`;
- `sidewalk_quality`;
- `stairs`;
- `crossings`;
- `transport_access`;
- a timestamp and time-dependent conditions.

The objective function is:

`Cost = w_time * t + w_sun * sun_exposure + w_sidewalk * penalty + w_stairs * penalty - w_greenery * greenery`

This makes it possible to use multi-objective routing and Pareto-optimal routes instead of selecting a single route based only on the shortest distance.

## Data Requirements

- OpenStreetMap (OSM);
- buildings and their geometry;
- roads and sidewalks;
- trees and green areas;
- crossings;
- public transport;
- elevation and terrain data;
- open municipal data.

Each dataset should be documented in a README with its source, collection date, quality level, and limitations.

## Research Hypothesis

Are Bishkek pedestrians willing to walk longer in exchange for a more comfortable route? The project will investigate:

- how often users choose a comfortable route;
- the acceptable increase in travel time;
- repeated use of a route;
- differences between days and times of day;
- how shade, greenery, and surface quality influence decisions.

For scenarios involving minors or privacy-sensitive users, only anonymized data should be used.

## Risks and Limitations

- the solar model is an estimate, not a physical measurement;
- full 3D modeling is not planned for the first stage;
- the project is not intended to provide real-time navigation;
- the MVP does not plan to include accounts, social features, advertising, or a mobile application;
- accuracy depends on the quality and freshness of the source geodata.

## Local Setup

1. Clone the repository:

```bash
git clone https://github.com/Lurish3/BishkekShadowMap.git
cd BishkekShadowMap
```

2. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Start the API:

```bash
uvicorn app.main:app --reload
```

5. Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

## Quality Checks

The project tests route logic and alternative route selection. Example checks include:

- correct route ordering;
- Pareto optimality;
- route recalculation based on time and conditions;
- prioritization of safety and comfort over speed alone.

## Roadmap

- **0.1:** basic A→B route, graph, solar model, time slider, and 2–3 alternatives;
- **0.2:** route weights, Pareto optimization, layers, route explanations, and route comparison;
- **0.3:** What-if scenarios, Simulate Walk, School Mode, transport, and analytics;
- **Later:** validation with real-world data, research into pedestrian behavior, and evaluation of the model’s value.

## What Makes This Project Strong for a Portfolio

This project combines several layers of value:

- urban analytics;
- GIS and spatial data;
- routing and optimization;
- mathematical modeling and multi-objective optimization;
- research methodology and product thinking;
- a clear business and social problem.

This is more than a mapping project. It is a product concept built around a real user problem: helping people choose routes that are not only fast, but also safer and more comfortable.

## Startup Value

The potential value of the project is not in creating another navigation app, but in developing a metric for the quality of pedestrian movement through the city. This can become part of urban infrastructure and a useful digital service for residents, rather than just another technical map.

## License

MIT

## Contact

The project is evolving from a research prototype into a working demonstration platform for urban comfort-aware routing.

Author: Lurish3

Repository: https://github.com/Lurish3/BishkekShadowMap

---

Bishkek Comfort Map is a dynamic, comfort-aware pedestrian routing prototype for Bishkek. The project does not aim to identify a single “best route”; it models trade-offs between speed, shade, greenery, pedestrian infrastructure, safety, and other route characteristics.

This is a portfolio-grade project built at the intersection of GIS, routing, environmental modeling, and product thinking.
