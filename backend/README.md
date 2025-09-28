# Backend

## Run (SQLite default)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Env Vars

- `DATABASE_URL` (optional): SQLAlchemy URL. Defaults to `sqlite:///./runs.db`
