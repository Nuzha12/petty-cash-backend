from sqlalchemy.orm import Session

from app.models.category import Category


def create_category(db: Session, data: dict):
    category = Category(**data)

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def get_categories_by_company(db: Session, company_id: int):
    return db.query(Category).filter(Category.company_id == company_id).all()


def get_category_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.category_id == category_id).first()


def delete_category(db: Session, category: Category):
    db.delete(category)
    db.commit()

    return category

