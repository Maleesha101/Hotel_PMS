"""Damage router – placeholder for future implementation."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import DamageReport
from app.schemas import DamageReportCreate, DamageReportRead
from uuid import UUID

router = APIRouter()

@router.post("/damage", response_model=DamageReportRead)
async def create_damage_report(report_in: DamageReportCreate, db: AsyncSession = Depends(get_db)):
    report = DamageReport(**report_in.model_dump())
    db.add(report)
    await db.flush()
    return report

@router.post("/damage/{report_id}/invoice", response_model=DamageReportRead)
async def send_to_invoice(report_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DamageReport).where(DamageReport.id == report_id))
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    report.status = "INVOICED"
    return report
