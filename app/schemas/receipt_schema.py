from pydantic import BaseModel


class ReceiptResponse(BaseModel):
    receipt_id: int
    expense_id: int
    file_url: str

    class Config:
        from_attributes = True

        
