from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models.gumba import Gumba
from app.models.role import Role
from app.models.user import User
from app.schemas.gumba import GumbaCreate


class GumbaService:

    @staticmethod
    def create_gumba(
        db: Session,
        gumba_data: GumbaCreate
    ):
        # Check whether this Gumba already exists
        existing_gumba = (
            db.query(Gumba)
            .filter(
                Gumba.name == gumba_data.name,
                Gumba.address == gumba_data.address,
                Gumba.district == gumba_data.district
            )
            .first()
        )

        if existing_gumba:
            raise HTTPException(
                status_code=409,
                detail="This Gumba is already registered."
            )
        # If an agent is provided, verify that
        # the user actually has AGENT role.
        if gumba_data.agent_id is not None:

            agent = (
                db.query(User)
                .join(Role)
                .filter(
                    User.id == gumba_data.agent_id,
                    Role.name == "AGENT",
                    User.is_active == True
                )
                .first()
            )

            if agent is None:
                raise HTTPException(
                    status_code=404,
                    detail="Active agent not found."
                )

        gumba = Gumba(
            name=gumba_data.name,
            description=gumba_data.description,
            address=gumba_data.address,
            district=gumba_data.district,
            municipality=gumba_data.municipality,
            ward_no=gumba_data.ward_no,
            contact_phone=gumba_data.contact_phone,
            contact_email=gumba_data.contact_email,
            website=gumba_data.website,
            latitude=gumba_data.latitude,
            longitude=gumba_data.longitude,
            photos=gumba_data.photos,
            videos=gumba_data.videos,
            agent_id=gumba_data.agent_id
        )

        db.add(gumba)
        db.commit()
        db.refresh(gumba)

        return gumba


    @staticmethod
    def get_gumba_by_id(
        db: Session,
        gumba_id: int
    ):

        gumba = (
            db.query(Gumba)
            .options(joinedload(Gumba.agent))
            .filter(
                Gumba.id == gumba_id,
                Gumba.is_active == True
            )
            .first()
        )

        if gumba is None:
            raise HTTPException(
                status_code=404,
                detail="Gumba not found."
            )

        return gumba

    @staticmethod
    def get_my_gumbas(
            db: Session,
            agent_id: int
    ):
        return (
            db.query(Gumba)
            .filter(
                Gumba.agent_id == agent_id,
                Gumba.is_active == True
            )
            .all()
        )

    @staticmethod
    def get_all_gumbas(db: Session):
        return (
            db.query(Gumba)
            .options(joinedload(Gumba.agent))
            .filter(Gumba.is_active == True)
            .all()
        )

    