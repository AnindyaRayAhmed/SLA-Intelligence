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

## 🚀 How to Run (2–3 minutes setup)
1. Download the project
```
Click Code → Download ZIP and extract it.
```

2. Open terminal in the folder
```
Inside the project folder, open Command Prompt / Terminal.
```

3. Install dependencies
   ```
pip install -r requirements.txt
```
4. Add your API key
```
Open the .env file and replace:

API_KEY=your_actual_key
```
5. Start the app
```
uvicorn backend.main:app --reload
```
6. Open in browser
```
Go to:
👉 http://127.0.0.1:8000/
```

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
