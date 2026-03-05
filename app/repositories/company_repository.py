from sqlalchemy.orm import Session
from app.models.company import Company


def create_company(db: Session, company: Company):

    db.add(company)
    db.commit()
    db.refresh(company)

    return company


def get_companies(db: Session, skip: int = 0, limit: int = 100):

    return db.query(Company).offset(skip).limit(limit).all()


def get_company_by_id(db: Session, company_id: int):

    return db.query(Company).filter(
        Company.company_id == company_id
    ).first()


def update_company(db: Session, company: Company):

    db.commit()
    db.refresh(company)

    return company


def delete_company(db: Session, company: Company):

    db.delete(company)
    db.commit()