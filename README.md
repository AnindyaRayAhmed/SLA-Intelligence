# AI SLA Intelligence Dashboard

Production-grade FastAPI + Pandas dashboard for SLA analytics from support ticket datasets.

## Features
- Upload CSV/Excel files with schema validation
- Automated data cleaning and standardization
- SLA evaluation based on configurable priority rules
- KPI tracking and interactive visualizations
- Agent, category, and channel-level performance insights
- AI-generated summaries and recommendations (structured, no raw data exposure)
- Clean dashboard UI using Jinja2 + Chart.js

__________________


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

________________________


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

_____________________________


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

____________________


# 📂 What you need to upload

Your file must include these columns:

- ticket_id
- agent_name
- created_at
- first_response_at
- resolved_at
- status
- priority
- category
- channel


# 📊 What the app does
- Calculates SLA performance
- Identifies delays and bottlenecks
- Compares agent performance
- Shows trends over time
- Generates AI-based insights and recommendations


# 🧠 Example Use Cases
- Customer support teams
- BPO operations
- Operations managers
- Project tracking


_____________________


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
