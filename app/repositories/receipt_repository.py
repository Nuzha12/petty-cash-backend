from sqlalchemy.orm import Session

from app.models.receipt import Receipt


def create_receipt(db: Session, expense_id: int, file_url: str):
    receipt = Receipt(
        expense_id= expense_id,
        file_url= file_url
    )

    db.add(receipt)
    db.commit()
    db.refresh(receipt)
    return receipt


def get_receipts_by_expense(db: Session, expense_id: int):
    return db.query(Receipt).filter(
        Receipt.expense_id == expense_id
    ).all()