from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TestResultBase(BaseModel):
    name: str
    status: str
    duration_ms: int = 0
    message: str = ""

class TestResultOut(TestResultBase):
    id: int
    class Config:
        from_attributes = True

class RunBase(BaseModel):
    name: str
    branch: str = ""
    commit_sha: str = ""

class RunCreate(RunBase):
    pass

class RunOut(RunBase):
    id: int
    status: str
    created_at: datetime
    started_at: datetime
    duration_seconds: float
    total_tests: int
    passed: int
    failed: int
    class Config:
        from_attributes = True

class RunDetail(RunOut):
    tests: List[TestResultOut] = []
