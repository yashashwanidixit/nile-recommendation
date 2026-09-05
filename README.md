# NILE — AI Itinerary & Recommendation Engine

**Stage 2 of 5** in the NILE AI-powered travel planning pipeline for South India, launching with the Bangalore → Goa corridor.

[![Tests](https://img.shields.io/badge/tests-38%2F38%20passing-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.13-blue)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-async-009688)]()

This service takes a customer's structured travel request and turns it into a personalized, day-by-day trip plan — filtering, scoring, and ranking hotels and activities before assembling them into a complete itinerary.

```
Customer Intent      Itinerary & Recommendation      Vendor Discovery      Vendor Intelligence      Vendor Partnership & Fulfillment
  (Jigisha)      →      (Yashaswini) ← this service   →     (Aman)     →       (Gargeyi)         →           (Vaibhav)
```

---

## What this service does

Once Jigisha's module converts a customer's raw request into structured intent — destination, dates, group size, budget, and preferences — this service is responsible for turning that into an actual plan:

1. **Filter** — narrow the full hotel and activity catalog down to what genuinely fits the customer's hard constraints (budget ceiling, group size, dates)
2. **Score & rank** — of what's left, rank options by how well they match softer preferences (style, amenities, activity type)
3. **Assemble an itinerary** — combine the best-fitting hotels and activities into a coherent, day-by-day plan
4. **Validate** — check the generated itinerary is internally consistent (no double-booked days, no budget overrun) before it's handed downstream

The output itinerary is passed to Aman's Vendor Discovery module, which finds and compares the real, bookable versions of what's been recommended.

---

## How a request flows through the system

```
                POST /recommendations/hotels
                POST /recommendations/activities
                POST /itinerary/generate
                              │
                              ▼
              UserIntent validated (Pydantic)
                              │
                              ▼
         Hotels / Activities loaded from catalog
         (cached in memory — parsed once, reused
          across requests via lru_cache)
                              │
                              ▼
                    services/filtering.py
              Hard constraints: budget, dates,
                   group size, availability
                              │
                              ▼
                     services/scoring.py
             Soft ranking: preference match,
                style fit, amenity relevance
                              │
                              ▼
                  services/recommendation.py
              Top-k hotels & activities selected
                              │
                              ▼
                    services/itinerary.py
              Day-by-day plan assembled from
                   the selected options
                              │
                              ▼
                   services/validation.py
              Sanity-checked before returning
                              │
                              ▼
              Typed response (HotelRecommendationResponse /
              ActivityRecommendationResponse / ItineraryResponse)
```

**Current status:** the API surface, data pipeline, validation schemas, configuration, and route wiring are fully built and tested. The core ranking logic in `filtering.py`, `scoring.py`, `recommendation.py`, and `itinerary.py` is scaffolded with clear function signatures and is the active area of development.

---

## What's implemented

| Area | Details |
|---|---|
| **Request validation** | Pydantic v2 schemas with real constraints — budget/group-size bounds, date-range validation (`end_date >= start_date`), regex-validated time strings for activity scheduling |
| **Catalog data pipeline** | Hotel and activity data loaded from JSON and validated into typed models on startup, cached in memory so large catalog files aren't re-parsed on every request |
| **Configuration** | Centralized settings via `pydantic-settings`, reading from `.env` — no hardcoded hosts, ports, or file paths |
| **API layer** | FastAPI routes with typed `response_model` contracts, dependency-injected cached data, CORS support, and global exception handling for clean error responses |
| **Core ranking logic** | Filtering, scoring, recommendation, and itinerary assembly — scaffolded and ready for the actual algorithm implementation |
| **LLM integration point** | An abstract `LLMClient` interface is in place for future use (e.g. natural-language itinerary summaries or prompt-based generation); no provider is wired in yet — this is a deliberate placeholder, not a gap |
| **Testing** | 38 tests covering schema validation, data loading, API contracts, config behavior, and route-to-service wiring |

---

## Tech stack

| Layer | Choice |
|---|---|
| API | Python, FastAPI |
| Data validation | Pydantic v2 |
| Configuration | pydantic-settings |
| Catalog storage | JSON (hotels, activities) — no database required at this stage |
| Testing | Pytest |

---

## Project structure

```
nile-recommendation/
├── main.py                     # FastAPI app, CORS, exception handlers, startup cache warm-up
├── core/
│   ├── config.py                 # Centralized settings (host, port, data paths, CORS, LLM config)
│   └── exceptions.py              # Domain exceptions + global error handlers
├── api/
│   └── routes/
│       ├── itinerary.py             # POST /itinerary/generate
│       └── recommendations.py       # POST /recommendations/hotels, /recommendations/activities
├── schemas/
│   ├── intent.py                    # UserIntent & preference models
│   ├── hotel.py                       # Hotel schema
│   ├── activity.py                    # Activity schema (time-window regex validation)
│   ├── itinerary.py                    # Itinerary, DayPlan, HotelPlan, ActivityPlan, ItineraryResponse
│   └── recommendation.py               # RecommendationItem, RecommendationOutput, response envelopes
├── services/
│   ├── data_loader.py               # Loads + caches hotel/activity catalogs
│   ├── filtering.py                   # Hard-constraint filtering (in development)
│   ├── scoring.py                       # Preference-based ranking (in development)
│   ├── recommendation.py                 # Top-k selection orchestration (in development)
│   ├── itinerary.py                        # Day-by-day itinerary assembly (in development)
│   └── validation.py                        # Itinerary sanity checks (in development)
├── llm/
│   ├── client.py                      # Abstract LLM provider interface
│   ├── prompts.py                       # Prompt construction (placeholder)
│   └── parser.py                          # LLM output parsing (placeholder)
├── data/
│   ├── hotels.json                    # Sample Goa hotel catalog
│   └── activities.json                  # Sample Goa activity catalog
├── postman/
│   └── NILE_Recommendation_API.postman_collection.json
└── tests/
    ├── test_api.py
    ├── test_config.py
    ├── test_filtering.py
    ├── test_itinerary.py
    ├── test_recommendation.py
    ├── test_scoring.py
    └── test_validation.py
```

---

## Getting started

### 1. Configure environment

```bash
cp .env.example .env
```

```bash
HOST=127.0.0.1
PORT=8000
ENVIRONMENT=development
CORS_ORIGINS=["*"]
HOTELS_DATA_PATH=data/hotels.json
ACTIVITIES_DATA_PATH=data/activities.json

# Reserved for future LLM integration — leave blank until a provider is chosen
LLM_API_KEY=
LLM_MODEL=
```

### 2. Install & run

```bash
pip install -r requirements.txt
python main.py
```

- API docs: `http://127.0.0.1:8000/docs`
- Health check: `GET /health`

### 3. Try it via Postman

Import `postman/NILE_Recommendation_API.postman_collection.json` for ready-made sample requests against every endpoint.

---

## Testing

```bash
pytest -v
```

38 tests, all passing:

| Suite | Covers |
|---|---|
| `test_validation.py` | Schema constraints — intent, hotel, activity, and data-loader validation |
| `test_api.py` | Endpoint contracts, status codes, CORS headers, route-to-service wiring |
| `test_config.py` | Default settings and environment variable overrides |
| `test_filtering.py`, `test_scoring.py`, `test_recommendation.py`, `test_itinerary.py` | Service-layer scaffolding and schema integration |

---

## API reference

### `POST /recommendations/hotels`
Returns hotel recommendations matching a customer's intent.

```json
{
  "destination": "Goa",
  "start_date": "2026-10-10",
  "end_date": "2026-10-14",
  "group_size": 4,
  "budget": 40000.0,
  "preferences": { "style": "beachfront", "amenities": ["pool", "wifi"] }
}
```

### `POST /recommendations/activities`
Returns activity recommendations for the trip window.

### `POST /itinerary/generate`
Assembles a full day-by-day itinerary from the customer's intent.

Full interactive documentation is available at `/docs` once the API is running.

---

## Design decisions worth knowing about

- **Why in-memory caching instead of a database?** At this stage, the catalog is a manageable JSON dataset. Parsing it once at startup and caching it with `lru_cache` avoids the cost of re-reading it per request without introducing database infrastructure before it's actually needed.
- **Why is the LLM client abstract with no provider wired in?** No provider (OpenAI, Gemini, Anthropic, etc.) has been decided yet. Keeping the interface abstract now means adding a real provider later is a contained change, not a rewrite.
- **Why do the routes call into stub service functions that return nothing yet?** So that once the actual filtering/scoring/itinerary logic is implemented, the API layer needs zero changes — the wiring, response shapes, and error handling are already correct and tested.

---

## Roadmap

- [ ] Implement hard-constraint filtering logic (`services/filtering.py`)
- [ ] Implement preference-based scoring and ranking (`services/scoring.py`)
- [ ] Implement itinerary assembly logic (`services/itinerary.py`)
- [ ] Implement itinerary validation rules (`services/validation.py`)
- [ ] Decide on and integrate an LLM provider for natural-language itinerary summaries
- [ ] Confirm the exact request schema with Jigisha (Customer Intent) and the exact output schema with Aman (Vendor Discovery)

---

## Part of NILE

This repository implements one stage of a five-stage system. See the pipeline overview above for how it fits alongside Customer Intent, Vendor Discovery, Vendor Intelligence, and Vendor Partnership & Fulfillment.
