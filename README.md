# FPGA Regression Dashboard

A small FastAPI backend + HTML/JS frontend to track FPGA/ASIC regression **runs** and per-test results. Create a run, upload a simulator log, and view pass/fail breakdowns in your browser.

---

![App Screenshot](https://github.com/DanKim15/FPGA-Regression-Dashboard/blob/main/dashboard_screenshot.png)

---

## Repository Structure

```
/ (root)
│
├─ backend/
│   ├─ app/
│   │   ├─ main.py           # FastAPI app: routes for runs, uploads, and run details
│   │   ├─ models.py         # SQLAlchemy ORM models: Run, TestResult
│   │   ├─ schemas.py        # Pydantic schemas: request/response JSONs
│   │   ├─ database.py       # Engine/session setup
│   │   └─ parser.py         # Log parser: extracts TEST ... PASS/FAIL and duration
│   └─ requirements.txt      # Backend dependencies
│
└─ frontend/
    ├─ index.html            # Minimal UI: forms + tables
    ├─ styles.css            # Light styling
    └─ app.js                # Fetches API data, updates DOM

```

---

## What It Does

- **Create runs** with name/branch/commit.
- **Upload logs** (`.log` / `.txt`) from ModelSim/Questa/ a bench output.
- **Parse tests** from lines like:
  ```
  TEST tb_1 ... PASS duration=12ms
  TEST tb_2 ... FAIL duration=3ms
  ```
- **Summaries** per run (total/passed/failed) and a **table of tests** (status, duration, message).

---

## Tech Stack

- **Backend:** FastAPI, Pydantic, SQLAlchemy ORM, SQLite
- **Frontend:** Plain HTML/CSS/JavaScript

---

## Setup (Windows, PowerShell)

1) **Backend**
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```
- API runs at: http://127.0.0.1:8000   
- Health: http://127.0.0.1:8000/health

2) **Frontend**
- Open `frontend/index.html` in your browser.

3) **Use it**
- Create a run, making note of the ID returned.
- Upload a log to that run.
- Click **View** to see per-test results.

> DB file: `backend/runs.db` is created automatically on the first write. Remove it to reset.

---

## API Overview

- `POST /runs` → **Create** a run  
  **Body** `{ "name": "run_01", "branch": "main", "commit_sha": "abc123" }`  
  **Returns** run info (includes `id`, timestamps, counters)

- `GET /runs` → **List** runs (id, name, status, total/passed/failed, created_at)

- `GET /runs/{id}` → **RunDetail** (run info + `tests` array)

- `POST /runs/{id}/logs` (multipart file) → **Upload** a log  
  **Form field**: `file` (text/log)  
  Parses results, updates DB, returns RunDetail

---

## Log Format (default parser)

- Recognizes lines matching:

```
TEST <name> ... PASS duration=12ms
TEST <name> ... FAIL duration=3ms
```

- Duration is optional (defaults to 0).  
- Non-matching lines are ignored.  

---


## TODO

- Filters: (PASS/FAIL), search, sort by duration or name
- Parse other log formats such as UVM summaries
