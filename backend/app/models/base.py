from sqlalchemy import Boolean, Column, DateTime, Integer, func


class BaseModelMixin:
    id = Column(Integer, primary_key=True, index=True)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
       nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    created_by = Column(Integer, nullable=True)

    updated_by = Column(Integer, nullable=True)


