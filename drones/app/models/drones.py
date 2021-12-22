from typing import Optional
from sqlmodel import Field
from enum import Enum, auto
from app.models import BaseModel
from sqlalchemy import UniqueConstraint


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


class DroneUpdate(BaseModel):
    serial_number: Optional[str]
    model: Optional[int]
    weight_limit: Optional[float]
    battery_capacity: Optional[float]
    state: DroneState = Optional[int]
