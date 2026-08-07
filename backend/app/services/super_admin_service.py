from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.role import Role
from app.models.user import User
from app.schemas.admin import AdminCreate
from sqlalchemy.orm import joinedload


class SuperAdminService:

    @staticmethod
    def create_admin(db: Session, admin: AdminCreate):

        existing = db.query(User).filter(
            User.email == admin.email
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        role = db.query(Role).filter(
            Role.name == "ADMIN"
        ).first()

        if role is None:
            raise HTTPException(
                status_code=404,
                detail="ADMIN role not found"
            )

        new_admin = User(
            full_name=admin.full_name,
            email=admin.email,
            phone=admin.phone,
            password=hash_password(admin.password),
            role_id=role.id
        )

        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)

        return new_admin

    @staticmethod
    def get_all_admins(db: Session):

        admins = (
            db.query(User)
            .join(Role)
            .options(joinedload(User.role))
            .filter(Role.name == "ADMIN")
            .all()
        )

        return admins