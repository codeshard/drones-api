from typing import List

from app.database import get_session
from app.models import Delivery, Medication, DeliveryCreate, Drone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

router = APIRouter(prefix="/deliveries", tags=["deliveries"])


@router.post("", response_model=Delivery)
async def create_delivery(
    *, deliver: DeliveryCreate, session: AsyncSession = Depends(get_session)
) -> Delivery:
    delivery_weight = 0
    result = await session.execute(select(Drone).where(Drone.id == deliver.drone_id))
    drone = result.scalar_one_or_none()
    if drone.state not in [1, 2]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The drone state {drone.state} is not allowed to execute deliveries!",
        )
    if drone.battery_level < 25:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The drone battery level {drone.battery_level} is to low to be loaded!",
        )
    for medication in deliver.medications:
        result = await session.execute(
            select(Medication).where(Medication.id == medication)
        )
        medication = result.scalar_one_or_none()
        delivery_weight += medication.weight
    if delivery_weight > drone.weight_limit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The medications weight {delivery_weight}gr is greater than the drone maximum weight {drone.weight_limit}gr!",
        )

    delivery = Delivery.from_orm(deliver)
    session.add(delivery)
    await session.commit()
    await session.refresh(delivery)

    drone.state = 3
    session.add(drone)
    await session.commit()
    await session.refresh(drone)

    for medication in deliver.medications:
        result = await session.execute(
            select(Medication).where(Medication.id == medication)
        )
        medication = result.scalar_one_or_none()
        medication.delivery_id = delivery.id
        session.add(medication)
        await session.commit()
        await session.refresh(medication)

    return delivery
