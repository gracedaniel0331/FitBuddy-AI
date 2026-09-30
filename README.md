# FitBuddy – AI Fitness Plan Generator using Gemini Models

FastAPI web app that generates a personalised 7-day workout plan (Gemini Pro), a nutrition/recovery tip
(Gemini Flash), refines the plan from user feedback, and stores everything in SQLite.

## Setup
```bash
python -m venv venv
venv\Scripts\activate          # Windows   (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env         # Linux/Mac: cp .env.example .env   -> then paste your GOOGLE_API_KEY
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000  (API docs: http://127.0.0.1:8000/docs)

Get a free Gemini API key at https://aistudio.google.com/app/apikey

## Free-tier note
If the Gemini free quota is used up, FitBuddy automatically creates the plan with a built-in planner
(`app/fallback_plan.py`) and marks it with a NOTE line. When Gemini works again, real AI plans are used.
The daily free quota resets about midnight Pacific time. A new API key from a new project also gives fresh quota.

## Pages / Routes
| Route | Purpose |
|---|---|
| `/` | Input form (index.html) |
| `/generate-workout` | Generate plan + nutrition tip (result.html) |
| `/submit-feedback` | Update plan from feedback |
| `/view-all-users` | Admin dashboard (all_users.html) |

## Structure
```
fitbuddy/
├── requirements.txt
├── .env.example
├── app/
│   ├── main.py  routes.py  database.py  schemas.py
│   ├── gemini_client.py  gemini_generator.py  gemini_flash_generator.py  updated_plan.py
│   ├── fallback_plan.py  nutrition.py
│   ├── templates/  (index.html, result.html, all_users.html)
│   └── static/images/gym-bg.jpg
└── fitbuddy.db  (auto-created)
```
