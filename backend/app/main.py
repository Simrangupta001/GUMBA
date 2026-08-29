from fastapi import FastAPI, HTTPException
from app.core.database import Base, engine
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from jose import JWTError
from app.exceptions.handlers import (
    http_exception_handler,
    validation_exception_handler,
    pydantic_validation_exception_handler,
    integrity_error_handler,
    sqlalchemy_error_handler,
    jwt_exception_handler,
    general_exception_handler,
)

import app.models
from app.routes.auth import router as auth_router
from app.routes.admin import router as admin_router
from app.routes.agent import router as agent_router
from app.routes.user import router as user_router
from app.routes.super_admin import router as super_admin_router
from app.middleware.logging import logging_middleware
from app.routes.gumba import router as gumba_router
from app.routes.donation import router as donation_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gumba Donation API")

@app.get("/")
def home():
    return {
        "message": "Gumba Backend Running "
    }
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(agent_router)
app.include_router(user_router)
app.include_router(super_admin_router)

app.add_exception_handler(
    HTTPException,
    http_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    ValidationError,
    pydantic_validation_exception_handler,
)

app.add_exception_handler(
    IntegrityError,
    integrity_error_handler,
)

app.add_exception_handler(
    SQLAlchemyError,
    sqlalchemy_error_handler,
)

app.add_exception_handler(
    JWTError,
    jwt_exception_handler,
)

app.add_exception_handler(
    Exception,
    general_exception_handler,
)

app.middleware("http")(logging_middleware)

app.include_router(gumba_router)
app.include_router(donation_router)







