from fastapi import FastAPI
from app.core.database import Base, engine

import app.models
from app.routes.auth import router as auth_router
from app.routes.admin import router as admin_router
from app.routes.agent import router as agent_router
from app.routes.user import router as user_router
from app.routes.super_admin import router as super_admin_router



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






