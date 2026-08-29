from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.role import Role
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already exists",
        )

    role = db.query(Role).filter(Role.name == "USER").first()

    if role is None:
        raise HTTPException(
            status_code=500,
            detail="USER role not found",
        )

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        password=hash_password(user.password),
        role_id=role.id,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Registration successful"}

#
# @router.post("/login")
# def login(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(get_db)
# ):
#     email = form_data.username
#     password = form_data.password
#
#     print("Email entered:", email)
#     print("Password entered:", password)
#     print("Connected DB:", db.bind.url)
#     users = db.query(User).all()
#
#     print("All users in DB:")
#     for u in users:
#         print(u.id, u.email)
#     db_user = db.query(User).filter(User.email == email).first()
#
#     print("Database user:", db_user)
#
#     if db_user:
#         print("Stored password:", db_user.password)
#
#     if not db_user:
#         raise HTTPException(status_code=401, detail="Invalid email or password")
#
#     print("Password verification:", verify_password(password, db_user.password))
#
#     if not verify_password(password, db_user.password):
#         raise HTTPException(status_code=401, detail="Invalid email or password")
#
#     token = create_access_token(db_user.id)
#
#     return {
#         "access_token": token,
#         "token_type": "bearer",
#         "role": db_user.role.name,
#     }


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    email = form_data.username
    password = form_data.password
    db_user = db.query(User).filter(
        User.email == email
    ).first()

    if not  db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(password,  db_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not  db_user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Your account is inactive. Please contact the administrator."
        )

    token = create_access_token(db_user.id)

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": db_user.role.name,
    }

@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role.name,
    }
