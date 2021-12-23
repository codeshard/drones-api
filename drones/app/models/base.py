import uuid
from datetime import datetime
from enum import Enum, auto
from typing import List, Optional
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel


class BaseModel(SQLModel):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default=datetime.now())


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
    deliveries: List["Delivery"] = Relationship(back_populates="drone")
    auditories: List["Auditory"] = Relationship(back_populates="drone")


class DroneCreate(SQLModel):
    serial_number: str
    model: Optional[DroneModel] = None
    weight_limit: float
    battery_capacity: float
    state: Optional[DroneState] = None


class DroneUpdate(SQLModel):
    serial_number: Optional[str] = None
    model: Optional[DroneModel] = None
    weight_limit: Optional[float] = None
    battery_capacity: Optional[float] = None
    state: Optional[DroneState] = None


class Delivery(BaseModel, table=True):
    __tablename__ = "deliveries"
    drone_id: Optional[uuid.UUID] = Field(default=None, foreign_key="drones.id")
    drone: Optional[Drone] = Relationship(back_populates="deliveries")
    medications: List["Medication"] = Relationship(back_populates="delivery")


class DeliveryCreate(SQLModel):
    drone_id: Optional[uuid.UUID] = None
    medications: Optional[List[uuid.UUID]] = None


class Medication(BaseModel, table=True):
    __tablename__ = "medications"
    __table_args__ = (UniqueConstraint("name"),)
    name: str = Field(..., index=True)
    weight: float = Field(..., gt=0)
    code: str = Field(..., index=True)
    image: str
    delivery_id: Optional[uuid.UUID] = Field(default=None, foreign_key="deliveries.id")
    delivery: Optional[Delivery] = Relationship(back_populates="medications")


class MedicationCreate(SQLModel):
    name: str = None
    weight: float = None
    code: str = None
    image: str = None


class MedicationUpdate(SQLModel):
    name: Optional[str] = None
    weigth: Optional[float] = Field(..., gt=0)
    code: Optional[str] = None
    image: Optional[str]


class Auditory(BaseModel, table=True):
    drone_id: Optional[uuid.UUID] = Field(default=None, foreign_key="drones.id")
    drone: Optional[Drone] = Relationship(back_populates="auditories")
    battery_capacity: float = Field(...)
