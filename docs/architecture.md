# docs/architecture.md

# Architecture overview

The project is designed around a simple but robust structure:

1. Data layer
   - raw OSM and GIS data
   - processed pedestrian network
   - environmental layers

2. Modeling layer
   - solar exposure model
   - green infrastructure model
   - sidewalk and crossing model
   - comfort score function

3. Routing layer
   - graph representation
   - route generation
   - Pareto evaluation
   - weighted route ranking

4. API layer
   - FastAPI service for endpoints and future frontend integration

5. Presentation layer
   - map interface with route alternatives and explanation panels

6. Research layer
   - empirical validation of user choices and route preferences

This architecture supports the product goal: route quality is not reduced to a single scalar, but evaluated through trade-offs visible to the user.
