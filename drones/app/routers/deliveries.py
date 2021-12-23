from typing import List

from app.database import get_session
from app.models import Delivery, DeliveryCreate, Drone, DroneState, Medication
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import and_, or_, select

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
            detail=f"The drone with ID {drone.id} and state {drone.state} is not allowed to execute deliveries!",
        )
    if drone.battery_capacity < 25:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The drone battery level {drone.battery_capacity} is to low to be loaded!",
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
            detail=f"The medications weight {delivery_weight}gr is greater than the drone maximum weight {drone.weight_limit}gr!",  # noqa
        )

    delivery = Delivery.from_orm(deliver)
    session.add(delivery)
    await session.commit()
    await session.refresh(delivery)

    drone.state = DroneState.LOADED
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


@router.get("/medications/{drone_id}", response_model=List[Medication])
async def medications_by_drone(
    drone_id: str, session: AsyncSession = Depends(get_session)
) -> List[Medication]:
    result = await session.execute(select(Drone).where(Drone.id == drone_id))
    drone = result.scalar_one_or_none()
    if drone.state not in [3, 4]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The drone with ID {drone_id} is not loaded or delivering!",
        )

    result = await session.execute(
        select(Delivery).where(Delivery.drone_id == drone_id)
    )
    delivery = result.scalar_one_or_none()
    if not delivery:
        raise HTTPException(
            status_code=404,
            detail=f"The drone with ID: {drone_id} has no active deliveries",
        )
    result = await session.execute(
        select(Medication).where(Medication.delivery_id == delivery.id)
    )
    medication_list = result.scalars().all()
    return medication_list


@router.get("/drones-availables", response_model=List[Drone])
async def list_available_drones(
    *, session: AsyncSession = Depends(get_session)
) -> List[Drone]:
    result = await session.execute(
        select(Drone).where(
            and_(
                Drone.battery_capacity >= 25,
                or_(
                    Drone.state == DroneState.IDLE,
                    Drone.state == DroneState.LOADING,
                ),
            )
        )
    )
    drones = result.scalars().all()
    return drones
