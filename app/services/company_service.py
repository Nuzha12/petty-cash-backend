from datetime import datetime
from sqlalchemy.orm import Session

from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate
from app.repositories import company_repository


def create_company(db: Session, company: CompanyCreate):

    new_company = Company(**company.model_dump())

    return company_repository.create_company(db, new_company)


def get_companies(db: Session, skip: int, limit: int):

    return company_repository.get_companies(db, skip, limit)


def get_company_by_id(db: Session, company_id: int):

    return company_repository.get_company_by_id(db, company_id)


def update_company_full(db: Session, db_company: Company, company: CompanyCreate):

    for key, value in company.model_dump().items():
        setattr(db_company, key, value)

    db_company.updated_at = datetime.utcnow()

    return company_repository.update_company(db, db_company)


def update_company_partial(db: Session, db_company: Company, company: CompanyUpdate):

    update_data = company.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_company, key, value)

    db_company.updated_at = datetime.utcnow()

    return company_repository.update_company(db, db_company)


def delete_company(db: Session, db_company: Company):

    company_repository.delete_company(db, db_company)