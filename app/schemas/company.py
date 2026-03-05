from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator, Field
import phonenumbers


class CompanyBase(BaseModel):
    company_name: str = Field(..., max_length=150)
    address: str | None = Field(default=None, max_length=255)
    contact: str | None = Field(default=None, max_length=20)

    @field_validator("contact", mode="before")
    @classmethod
    def validate_phone(cls, value):

        if value is None:
            return value

        try:
            # Default region Sri Lanka
            phone = phonenumbers.parse(value, "LK")

            if not phonenumbers.is_valid_number(phone):
                raise ValueError("Invalid phone number")

            return phonenumbers.format_number(
                phone,
                phonenumbers.PhoneNumberFormat.E164
            )

        except phonenumbers.NumberParseException:
            raise ValueError("Invalid phone number format")


class CompanyCreate(CompanyBase):
    pass


class CompanyResponse(CompanyBase):
    company_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CompanyUpdate(BaseModel):
    company_name: str | None = None
    address: str | None = None
    contact: str | None = None

