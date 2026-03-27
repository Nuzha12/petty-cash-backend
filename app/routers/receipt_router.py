from fastapi import APIRouter, UploadFile, File
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import verify_token
from app.database import get_db
from app.services import receipt_service

router = APIRouter(prefix="/receipts", tags=["receipts"])

@router.post("/upload")
def upload_receipt(expense_id: int, file: UploadFile = File(...), db: Session= Depends(get_db), manager = Depends(verify_token)):
    return receipt_service.upload_receipt(db, expense_id, file, manager)


@router.get("/{expense_id}")
def get_receipts(expense_id: int, db: Session= Depends(get_db), manager= Depends(verify_token)):
    return receipt_service.get_receipts(db, expense_id)

