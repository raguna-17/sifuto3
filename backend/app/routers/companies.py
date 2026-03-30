from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db import get_db
from app.schemas import CompanyRead, CompanyCreate
from app.services import company_service

router = APIRouter(prefix="/api/v1/companies", tags=["companies"])

# 一覧
@router.get("/", response_model=List[CompanyRead])
async def get_companies(db: AsyncSession = Depends(get_db)):
    # applicationsも事前ロード済み
    return await company_service.get_companies(db)

# 単体
@router.get("/{company_id}", response_model=CompanyRead)
async def get_company(company_id: int, db: AsyncSession = Depends(get_db)):
    company = await company_service.get_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

# 作成
@router.post("/", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
async def create_company(company: CompanyCreate, db: AsyncSession = Depends(get_db)):
    existing = await company_service.get_company_by_name(db, company.name)
    if existing:
        raise HTTPException(status_code=400, detail="Company already exists")
    return await company_service.create_company(db, company.model_dump())

# 削除
@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: int, db: AsyncSession = Depends(get_db)):
    company = await company_service.delete_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)