from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Run(Base):
    __tablename__ = "runs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    branch = Column(String, default="")
    commit_sha = Column(String, default="")
    status = Column(String, default="created")
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, default=datetime.utcnow)
    duration_seconds = Column(Float, default=0.0)
    total_tests = Column(Integer, default=0)
    passed = Column(Integer, default=0)
    failed = Column(Integer, default=0)

    tests = relationship(
        "TestResult", back_populates="run", cascade="all,delete")


class TestResult(Base):
    __tablename__ = "test_results"
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("runs.id"))
    name = Column(String, index=True)
    status = Column(String)  # PASS/FAIL
    duration_ms = Column(Integer, default=0)
    message = Column(String, default="")

    run = relationship("Run", back_populates="tests")
