import mimetypes
import os
import shutil
import uuid

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.models import Expense
from app.repositories import receipt_repository

UPLOAD_DIR = "uploads/receipts"
MAX_FILE_SIZE = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


def get_extension(file: UploadFile):
    if file.filename and "." in file.filename:
        ext = file.filename.rsplit(".", 1)[-1].lower()
        return ext

    content_type = file.content_type
    ext = mimetypes.guess_extension(content_type)

    if ext:
        return ext.replace(".", "")

    raise HTTPException(status_code=400, detail="Cannot determine file extension")


def validate_file(file: UploadFile):
    ext = get_extension(file)

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")

    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)

    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")


def generate_unique_filename(file: UploadFile):
    ext = get_extension(file)
    return f"{uuid.uuid4().hex}.{ext}"


def save_file(file: UploadFile):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    validate_file(file)

    filename = generate_unique_filename(file)
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return f"/uploads/receipts/{os.path.basename(file_path)}"


def upload_receipt(db: Session, expense_id: int, file: UploadFile, manager):
    expense = db.query(Expense).filter(
        Expense.expense_id == expense_id,
        Expense.company_id == manager.company_id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    file_url = save_file(file)

    return receipt_repository.create_receipt(db, expense_id, file_url)


def get_receipts(db: Session, expense_id: int):
    return receipt_repository.get_receipts_by_expense(db, expense_id)