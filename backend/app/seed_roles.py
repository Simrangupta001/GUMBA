from app.core.database import SessionLocal
from app.models.role import Role

db = SessionLocal()

roles = [
    "SUPER_ADMIN",
    "ADMIN",
    "AGENT",
    "USER",
]

for role_name in roles:
    exists = db.query(Role).filter(Role.name == role_name).first()

    if not exists:
        db.add(Role(name=role_name))

db.commit()

print("Roles inserted successfully.")