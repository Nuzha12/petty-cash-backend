from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories import category_repository
from app.schemas.category import CategoryCreate


def create_category(db: Session, category: CategoryCreate, user):

    category_data = category.model_dump()

    category_data["company_id"] = user["company_id"]

    try:
        return category_repository.create_category(db, category_data)

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Category already exists for this company")



def get_categories(db: Session, user):

    return category_repository.get_categories_by_company(db, user["company_id"])


def delete_category(db: Session, category_id: int, user):

    category = category_repository.get_category_by_id(db, category_id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category.company_id != user["company_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    return category_repository.delete_category(db, category)