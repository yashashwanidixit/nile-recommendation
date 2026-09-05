# NILE Recommendation Engine

The **NILE AI Itinerary & Recommendation Engine** provides travel recommendations and structured itinerary generation for personalized trip experiences.

## Pipeline Architecture

```text
User Intent
     ↓
Load Hotels + Activities
     ↓
Hard Filtering
     ↓
Soft Scoring / Ranking
     ↓
Top-K Recommendations
     ↓
LLM Itinerary Generation
     ↓
JSON Validation
     ↓
Final Itinerary JSON
```

## Current Scope & Foundation

This repository currently provides the foundational architecture and data contracts:

* **Pydantic Schemas (`schemas/`)**:
  * `UserIntent` & `Preferences`: Strict input travel contracts.
  * `Hotel`: Strict vendor hotel model with geographic, capacity, and price constraints.
  * `Activity`: Strict vendor activity model with operational hours and category constraints.
  * `RecommendationItem` & `RecommendationOutput`: Output contracts for deterministic ranking.
  * `ActivityPlan`, `DayPlan`, `HotelPlan`, & `Itinerary`: Contract for LLM-generated structured itineraries.
* **Sample Datasets (`data/`)**:
  * `hotels.json`: Valid sample Goa hotel records.
  * `activities.json`: Valid sample Goa activity records.
* **Data Loading (`services/data_loader.py`)**:
  * Validated ingestion of JSON datasets into Pydantic models.
* **Service Placeholders (`services/`)**:
  * `filtering.py`: Hard constraint filtering signatures.
  * `scoring.py`: Soft scoring and ranking signatures.
  * `recommendation.py`: Recommendation orchestration signatures.
  * `itinerary.py`: Itinerary generation orchestration signatures.
  * `validation.py`: Deterministic validation signatures.
* **LLM Abstraction (`llm/`)**:
  * `client.py`: LLM client interface.
  * `prompts.py`: Prompt builder signature.
  * `parser.py`: Itinerary JSON parsing signature.
* **Test Suite (`tests/`)**:
  * Pytest coverage for schema validations, edge cases, and data loading.

> **Note**: Recommendation, scoring, filtering, and LLM generation logic will be implemented in subsequent development stages.

## Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Tests
```bash
pytest
```

### 3. Verify Foundation Setup
```bash
python main.py
```
