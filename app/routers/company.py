from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT

from app.database import get_db
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate
from app.services import company_service


router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("/", response_model=CompanyResponse)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    return company_service.create_company(db, company)


@router.get("/", response_model=list[CompanyResponse])
def get_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return company_service.get_companies(db, skip, limit)


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(company_id: int, db: Session = Depends(get_db)):

    company = company_service.get_company_by_id(db, company_id)

    if not company:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Company not found"
        )

    return company


@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(company_id: int, company: CompanyCreate, db: Session = Depends(get_db)):

    db_company = company_service.get_company_by_id(db, company_id)

    if not db_company:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Company not found"
        )

    return company_service.update_company_full(db, db_company, company)


@router.patch("/{company_id}", response_model=CompanyResponse)
def update_company_partial(company_id: int, company: CompanyUpdate, db: Session = Depends(get_db)):

    db_company = company_service.get_company_by_id(db, company_id)

    if not db_company:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Company not found"
        )

    return company_service.update_company_partial(db, db_company, company)


@router.delete("/{company_id}", status_code=HTTP_204_NO_CONTENT)
def delete_company(company_id: int, db: Session = Depends(get_db)):

    db_company = company_service.get_company_by_id(db, company_id)

    if not db_company:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Company not found"
        )

    company_service.delete_company(db, db_company)