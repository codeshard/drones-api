from typing import Optional

from app.models import BaseModel
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel


class Medication(BaseModel, table=True):
    __tablename__ = "medications"
    __table_args__ = (UniqueConstraint("name"),)
    name: str = Field(index=True)
    weight: float = Field(gt=0)
    code: str = Field(index=True)
    image: str


class MedicationUpdate(SQLModel):
    name: Optional[str] = None
    weigth: Optional[float] = None
    code: Optional[str] = None
    image: Optional[str]
