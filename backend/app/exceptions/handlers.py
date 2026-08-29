from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from jose import JWTError
from pydantic import ValidationError


def http_exception_handler(
    request: Request,
    exc: HTTPException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": str(exc.detail),
            "errors": None,
        },
    )


def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    errors = {}

    for error in exc.errors():
        field = ".".join(str(location) for location in error["loc"])
        errors[field] = error["msg"]

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation failed.",
            "errors": errors,
        },
    )


def pydantic_validation_exception_handler(
    request: Request,
    exc: ValidationError,
):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation failed.",
            "errors": exc.errors(),
        },
    )


def integrity_error_handler(
    request: Request,
    exc: IntegrityError,
):
    return JSONResponse(
        status_code=409,
        content={
            "success": False,
            "message": "Database constraint violation.",
            "errors": None,
        },
    )


def sqlalchemy_error_handler(
    request: Request,
    exc: SQLAlchemyError,
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Database error.",
            "errors": None,
        },
    )


def jwt_exception_handler(
    request: Request,
    exc: JWTError,
):
    return JSONResponse(
        status_code=401,
        content={
            "success": False,
            "message": "Invalid or expired authentication token.",
            "errors": None,
        },
    )




def general_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error.",
            "errors": None,
        },
    )

