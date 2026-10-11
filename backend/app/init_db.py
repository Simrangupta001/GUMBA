import time

from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import configure_mappers

import app.models  # noqa: F401
from app.core.database import Base, SessionLocal, engine
from app.models.role import Role

ROLES = ["SUPER_ADMIN", "ADMIN", "AGENT", "USER"]


def wait_for_db(retries=30, delay=2.0):
    for attempt in range(1, retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except OperationalError:
            print(f"[init_db] Database not ready ({attempt}/{retries}), retrying...")
            time.sleep(delay)
    raise SystemExit("[init_db] Database never became reachable.")


def init():
    wait_for_db()
    configure_mappers()
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        for name in ROLES:
            if not db.query(Role).filter(Role.name == name).first():
                db.add(Role(name=name))
        db.commit()
    finally:
        db.close()

    print("[init_db] Database ready.")


if __name__ == "__main__":
    init()