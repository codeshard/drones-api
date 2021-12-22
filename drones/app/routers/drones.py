from typing import List

from app.database import engine, get_session
from app.models import Drone
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session, select

router = APIRouter(prefix="/drones", tags=["drones"])


@router.post("", response_model=Drone)
async def create_drone(
    drone: Drone, session: AsyncSession = Depends(get_session)
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
    dron = Drone(
        serial_number=drone.serial_number,
        model=drone.model,
        weight_limit=drone.weight_limit,
        battery_capacity=drone.battery_capacity,
        state=drone.state,
    )
    session.add(dron)
    await session.commit()
    await session.refresh(dron)
    return dron


@router.get("/id", response_model=Drone)
async def retrieve_drone(id: str) -> Drone:
    with Session(engine) as session:
        return session.get(Drone, id)


@router.patch("/id", response_model=Drone)
async def update_drone(id: str) -> Drone:
    pass


@router.post("/id", response_model=Drone)
async def delete_drone(id: str) -> Drone:
    pass


@router.get("", response_model=List[Drone])
async def list_drones(session: AsyncSession = Depends(get_session)) -> List[Drone]:
    result = await session.execute(select(Drone))
    drones = result.scalars().all()
    return [
        Drone(
            id=drone.id,
            serial_number=drone.serial_number,
            model=drone.model,
            weight_limit=drone.weight_limit,
            battery_capacity=drone.battery_capacity,
            state=drone.state,
            created_at=drone.created_at,
        )
        for drone in drones
    ]
