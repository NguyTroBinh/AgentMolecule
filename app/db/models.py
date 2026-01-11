# app/db/models.py

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON
from typing import Optional, List, Dict, Any
from datetime import datetime

# Luu tru thong tin ve cac luot chay va cac phan tu tim duoc

class MoleculeRun(SQLModel, table=True):
    # Luu tru thong tin tong quat ve mot luot chay
    id: Optional[str] = Field(default=None, primary_key=True)
    objective: str
    status: str = "PENDING"  # PENDING, RUNNING, COMPLETED, FAILED
    current_round: int = 0
    max_rounds: int = 3
    filters: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    logs: List[str] = Field(default=[], sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
class MoleculeResult(SQLModel, table=True):
    # Luu tru thong tin ve cac phan tu hoa hoc tim duoc
    id: Optional[int] = Field(default=None, primary_key=True)
    run_id: str = Field(foreign_key="moleculerun.id")
    smiles: str
    mw: float
    logp: float
    qed: float
    score: float
    violations: int
    properties: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))