# AI SLA Intelligence Dashboard

Production-grade FastAPI + Pandas dashboard for SLA analytics from support ticket datasets.

## Features
- CSV/Excel upload with strict schema validation.
- Data cleaning pipeline with standardized fields and row-level resilience.
- Dynamic SLA evaluation by priority from JSON config.
- KPI, chart-ready aggregates, and searchable/filterable table output.
- Deterministic insights generator based on structured summary only (no raw dataset exposure).
- Server-rendered dashboard with Jinja2 + vanilla JS + Chart.js.

## Project Structure
```
backend/
  main.py
  api/routes.py
  services/{cleaner.py, metrics.py, sla.py, insights.py}
  schemas/ticket_schema.py
  config/sla.json
  utils/helpers.py
  core/settings.py
frontend/
  templates/index.html
  static/css/style.css
  static/js/app.js
.env
requirements.txt
```

## Required Input Columns
- ticket_id
- agent_name
- created_at
- first_response_at
- resolved_at
- status
- priority
- category
- channel

## Run Locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure environment variables in `.env`.
3. Start app:
   ```bash
   uvicorn backend.main:app --reload
   ```
4. Open:
   - `http://127.0.0.1:8000/`

## API
### `GET /`
Renders dashboard.

### `POST /upload`
Accepts multipart file (`.csv`, `.xlsx`, `.xls`) and returns:
- `kpis`
- `charts`
- `insights`
- `table_data`
- `warnings`
