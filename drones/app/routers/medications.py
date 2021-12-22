from typing import List

from app.database import get_session
from app.models import Medication, MedicationUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

router = APIRouter(prefix="/medications", tags=["medications"])


@router.post("", response_model=Medication)
async def create_medication(
    *, med: Medication, session: AsyncSession = Depends(get_session)
) -> Medication:
    medication = Medication.from_orm(med)
    session.add(medication)
    await session.commit()
    await session.refresh(medication)
    return medication


@router.get("/{medication_id}", response_model=Medication)
async def retrieve_medication(
    *, medication_id: str, session: AsyncSession = Depends(get_session)
) -> Medication:
    result = await session.execute(
        select(Medication).where(Medication.id == medication_id)
    )
    medication = result.scalar_one_or_none()
    if not medication:
        raise HTTPException(
            status_code=404, detail=f"Medication {medication_id} not found"
        )
    return medication


@router.patch("/{medication_id}", response_model=Medication)
async def update_medication(
    *,
    medication_id: str,
    patch: MedicationUpdate,
    session: AsyncSession = Depends(get_session),
) -> Medication:
    result = await session.execute(
        select(Medication).where(Medication.id == medication_id)
    )
    medication = result.scalar_one_or_none()
    if not medication:
        raise HTTPException(
            status_code=404, detail=f"Medication {medication_id} not found"
        )
    patch_data = patch.dict(exclude_unset=True)
    for key, value in patch_data.items():
        setattr(medication, key, value)
    session.add(medication)
    await session.commit()
    await session.refresh(medication)
    return medication


@router.post("/{medication_id}")
async def delete_medication(
    *, medication_id: str, session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Medication).where(Medication.id == medication_id)
    )
    medication = result.scalar_one_or_none()
    if not medication:
        raise HTTPException(
            status_code=404, detail=f"Medication {medication_id} not found"
        )
    session.delete(medication)
    await session.commit()
    return {"ok": True}


@router.get("", response_model=List[Medication])
async def list_medications(
    *, session: AsyncSession = Depends(get_session)
) -> List[Medication]:
    result = await session.execute(select(Medication))
    medications = result.scalars().all()
    return medications
