from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from .database import Base, engine, SessionLocal
from . import models, schemas, parser

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FPGA Regression Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/runs", response_model=schemas.RunOut)
def create_run(run: schemas.RunCreate, db: Session = Depends(get_db)):
    r = models.Run(name=run.name, branch=run.branch,
                   commit_sha=run.commit_sha, status="created")
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


@app.get("/runs", response_model=List[schemas.RunOut])
def list_runs(db: Session = Depends(get_db)):
    return db.query(models.Run).order_by(models.Run.created_at.desc()).all()


@app.get("/runs/{run_id}", response_model=schemas.RunDetail)
def get_run(run_id: int, db: Session = Depends(get_db)):
    r = db.query(models.Run).filter(models.Run.id == run_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Run not found")
    return r


@app.post("/runs/{run_id}/logs", response_model=schemas.RunDetail)
async def upload_log(run_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    r = db.query(models.Run).filter(models.Run.id == run_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Run not found")
    content = (await file.read()).decode("utf-8", errors="ignore")
    r.status = "parsing"
    db.commit()

    parsed = parser.parse_log(content)
    # Clear previous tests
    db.query(models.TestResult).filter(
        models.TestResult.run_id == run_id).delete()
    # Insert new tests
    for t in parsed['tests']:
        db.add(models.TestResult(run_id=run_id, **t))

    r.passed = parsed['passed']
    r.failed = parsed['failed']
    r.total_tests = parsed['total']
    r.status = "complete"
    db.commit()
    db.refresh(r)
    return r
