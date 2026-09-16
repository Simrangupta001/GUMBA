from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_password_reset_token,
    decode_password_reset_token,
    hash_password,
    verify_password,
    password_fingerprint,
)
from app.models.role import Role
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserLogin,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.services.email_service import EmailService

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

@router.post("/forgot-password")
def forgot_password(
    payload: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == payload.email).first()

    # Always return the same response whether or not the email is
    # registered, so this endpoint can't be used to check which
    # emails exist in the system.
    generic_response = {
        "message": (
            "If an account with that email exists, a password "
            "reset link has been sent."
        )
    }

    if user is None or not user.is_active:
        return generic_response

    token = create_password_reset_token(user)

    reset_link = (
        f"{settings.FRONTEND_RESET_PASSWORD_URL}?token={token}"
        if settings.FRONTEND_RESET_PASSWORD_URL
        else None
    )

    EmailService.send_templated_email(
        to=user.email,
        subject="Reset your GUMBA password",
        template_name="password_reset.html",
        context={
            "greeting_name": user.full_name,
            "reset_link": reset_link,
            "reset_token": token,
            "expire_minutes": settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES,
        },
    )

    return generic_response


@router.post("/reset-password")
def reset_password(
    payload: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    invalid_link_error = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid or expired reset link. Please request a new one.",
    )

    try:
        token_payload = decode_password_reset_token(payload.token)
    except JWTError:
        raise invalid_link_error

    user_id = token_payload.get("sub")

    if user_id is None:
        raise invalid_link_error

    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None or not user.is_active:
        raise invalid_link_error

    # The fingerprint was computed from the user's password hash at
    # the moment this token was issued. If the password has changed
    # since then (via this same link already being used once, or by
    # any other means), the fingerprint no longer matches - so this
    # token is treated as already used / no longer valid.
    if password_fingerprint(user.password) != token_payload.get("pwd_fp"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "This reset link has already been used or is no "
                "longer valid. Please request a new one."
            ),
        )

    user.password = hash_password(payload.new_password)

    db.commit()

    # Notify the user their password changed, after the commit has
    # already succeeded - same "never email before the DB write is
    # safe" rule used for donations and agent applications.
    EmailService.send_templated_email(
        to=user.email,
        subject="Your GUMBA password was changed",
        template_name="password_changed.html",
        context={"greeting_name": user.full_name},
    )

    return {
        "message": (
            "Password has been reset successfully. "
            "You can now log in with your new password."
        )
    }
