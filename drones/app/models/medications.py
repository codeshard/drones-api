from sqlmodel import Field
from app.models import BaseModel


class Medication(BaseModel, table=True):
    __tablename__ = "medications"
    name: str = Field(index=True)
    weight: float = Field(gt=0)
    code: str = Field(index=True)
    image: str
