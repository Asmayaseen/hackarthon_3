from typing import Optional, List
from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import datetime

class Severity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class AlertType(str, Enum):
    completion_rate = "completion_rate"
    repeated_failures = "repeated_failures"
    low_scores = "low_scores"

class StruggleAlert(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: str
    alert_type: AlertType
    severity: Severity
    message: str
    recommendations: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    resolved: bool = False
