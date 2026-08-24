from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import admin_required
from app.models.user import User

from app.schemas.gumba import (
    GumbaCreate,
    GumbaResponse
)

from app.services.gumba_service import GumbaService


router = APIRouter(
    prefix="/gumbas",
    tags=["Gumba"]
)


@router.post(
    "",
    response_model=GumbaResponse
)
def create_gumba(
    gumba: GumbaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):

    return GumbaService.create_gumba(
        db,
        gumba
    )


@router.get(
    "",
    response_model=List[GumbaResponse]
)
def get_gumbas(
    db: Session = Depends(get_db)
):

    return GumbaService.get_all_gumbas(db)


@router.get(
    "/{gumba_id}",
    response_model=GumbaResponse
)
def get_gumba(
    gumba_id: int,
    db: Session = Depends(get_db)
):

    return GumbaService.get_gumba_by_id(
        db,
        gumba_id
    )