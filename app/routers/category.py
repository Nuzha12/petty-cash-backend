from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import verify_token
from app.database import get_db
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services import category_service

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db), user= Depends(verify_token)):
    return category_service.create_category(db, category, user)


@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db), user = Depends(verify_token)):
    return category_service.get_categories(db, user)


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db), user = Depends(verify_token)):
    category_service.delete_category(db, category_id, user)

    return {"message": "Category deleted successfully"}
