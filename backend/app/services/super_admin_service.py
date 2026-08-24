from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.role import Role
from app.models.user import User
from app.schemas.admin import AdminCreate, AdminUpdate, AdminStatusUpdate
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

    @staticmethod
    def get_admin_by_id(db: Session, admin_id: int):

        admin = (
            db.query(User)
            .join(Role)
            .options(joinedload(User.role))
            .filter(
                User.id == admin_id,
                Role.name == "ADMIN"
            )
            .first()
        )

        if admin is None:
            raise HTTPException(
                status_code=404,
                detail="Admin not found"
            )

        return admin

    @staticmethod
    def update_admin(
            db: Session,
            admin_id: int,
            admin_data: AdminUpdate
    ):
        admin = (
            db.query(User)
            .join(Role)
            .filter(
                User.id == admin_id,
                Role.name == "ADMIN"
            )
            .first()
        )

        if admin is None:
            raise HTTPException(
                status_code=404,
                detail="Admin not found"
            )

        update_data = admin_data.model_dump(
            exclude_unset=True
        )

        if "full_name" in update_data:
            admin.full_name = update_data["full_name"]

        if "email" in update_data:
            admin.email = update_data["email"]

        if "phone" in update_data:
            admin.phone = update_data["phone"]

        if "password" in update_data:
            admin.password = hash_password(
                update_data["password"]
            )

        if "is_active" in update_data:
            admin.is_active = update_data["is_active"]

        db.commit()
        db.refresh(admin)

        return admin

    @staticmethod
    def update_admin_status(
            db: Session,
            admin_id: int,
            status_data: AdminStatusUpdate
    ):
        admin = (
            db.query(User)
            .join(Role)
            .filter(
                User.id == admin_id,
                Role.name == "ADMIN"
            )
            .first()
        )

        if admin is None:
            raise HTTPException(
                status_code=404,
                detail="Admin not found"
            )

        admin.is_active = status_data.is_active

        db.commit()
        db.refresh(admin)

        return admin


    # @staticmethod
    # def get_admin(db: Session, admin_id: int):
    #     admin = db.query(User).filter(
    #         User.id == admin_id,
    #         User.role.has(name="ADMIN")
    #     ).first()
    #
    #     if not admin:
    #         raise HTTPException(
    #             status_code=404,
    #             detail="Admin not found"
    #         )
    #
    #     return admin