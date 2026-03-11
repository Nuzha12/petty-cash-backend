from sqlalchemy.orm import Session

from app.repositories.manager_repository import get_manager_by_email
from app.auth.jwt_handler import create_access_token
from app.core.security import verify_password


def login_manager(db: Session, email: str, password: str):

    manager = get_manager_by_email(db, email)

    if not manager:
        return None

    if not verify_password(password, manager.password):
        return None

    token = create_access_token(
        {
            "manager_id": manager.manager_id,
            "company_id": manager.company_id
        }
    )

    return token