from typing import List

from app.database import engine, get_session
from app.jobs import schedule
from app.models import Auditory, Drone, DroneUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

router = APIRouter(prefix="/drones", tags=["drones"])


@schedule.scheduled_job("interval", minutes=0.5, id="check-battery-state")
async def check_drones_battery():
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Drone))
        drones = result.scalars().all()
        for drone in drones:
            auditory = Auditory(
                drone_id=drone.id, battery_capacity=drone.battery_capacity
            )
            session.add(auditory)
            await session.commit()
            await session.refresh(auditory)


@router.post("", response_model=Drone)
async def create_drone(
    *, drone: Drone, session: AsyncSession = Depends(get_session)
) -> Drone:
    """
    Create a drone using the given params
    * **Serial Number**: Alphanumeric identification of the drone, unique value.
    * Model: integer value, to choose between.
        * 1 - Lightweight
        * 2 - Middleweight
        * 3 - Cruiserweight
        * 4 - Heavyweight

      Default value: 1 (*Lightweight*)
    * **Weight Limit**: decimal value. Minimum value allowed *0* and maximum value allowed *500*.
    * **Battery Capacity**: integer value. Minimum value allowed *0* and maximum value allowed *100*.
    * State: integer value, to choose between.
        * 1 - Idle
        * 2 - Loading
        * 3 - Loaded
        * 4 - Delivering
        * 5 - Delived
        * 6 - Returning

      Default value: 1 (*Idle*)
    """
    dron = Drone.from_orm(drone)
    session.add(dron)
    await session.commit()
    await session.refresh(dron)
    return dron


@router.get("/{drone_id}", response_model=Drone)
async def retrieve_drone(
    *, drone_id: str, session: AsyncSession = Depends(get_session)
) -> Drone:
    result = await session.execute(select(Drone).where(Drone.id == drone_id))
    drone = result.scalar_one_or_none()
    if not drone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Drone not found"
        )
    return drone


@router.patch("/{drone_id}", response_model=Drone)
async def update_drone(
    *, drone_id: str, patch: DroneUpdate, session: AsyncSession = Depends(get_session)
) -> Drone:
    result = await session.execute(select(Drone).where(Drone.id == drone_id))
    drone = result.scalar_one_or_none()
    if not drone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Drone not found"
        )
    patch_data = patch.dict(exclude_unset=True)
    for key, value in patch_data.items():
        setattr(drone, key, value)
    session.add(drone)
    await session.commit()
    await session.refresh(drone)
    return drone


@router.post("/{drone_id}")
async def delete_drone(*, drone_id: str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Drone).where(Drone.id == drone_id))
    drone = result.scalar_one_or_none()
    if not drone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Drone not found"
        )
    session.delete(drone)
    await session.commit()
    return {"ok": True}


@router.get("", response_model=List[Drone])
async def list_drones(*, session: AsyncSession = Depends(get_session)) -> List[Drone]:
    result = await session.execute(select(Drone))
    drones = result.scalars().all()
    return drones
