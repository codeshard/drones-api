from enum import Enum, auto
from typing import Optional

from app.models import BaseModel
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel


class DroneModel(int, Enum):
    LIGHTWEIGHT = auto()
    MIDDLEWEIGHT = auto()
    CRUISERWEIGHT = auto()
    HEAVYWEIGHT = auto()


class DroneState(int, Enum):
    IDLE = auto()
    LOADING = auto()
    LOADED = auto()
    DELIVERING = auto()
    DELIVERED = auto()
    RETURNING = auto()


class Drone(BaseModel, table=True):
    __tablename__ = "drones"
    __table_args__ = (UniqueConstraint("serial_number"),)
    serial_number: str = Field(..., max_length=100, index=True)
    model: DroneModel = DroneModel.LIGHTWEIGHT
    weight_limit: float = Field(..., ge=0, le=500)
    battery_capacity: float = Field(..., ge=0, le=100)
    state: DroneState = DroneState.IDLE


class DroneUpdate(SQLModel):
    serial_number: Optional[str] = None
    model: Optional[DroneModel] = None
    weight_limit: Optional[float] = None
    battery_capacity: Optional[float] = None
    state: Optional[DroneState] = None
