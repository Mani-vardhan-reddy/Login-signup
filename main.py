from app.database.database import Base, engine, SessionLocal
from fastapi import FastAPI
import uvicorn
from app.routes.signup_routes import router
from app.notifications_trmplates.templates_seeders_data import TemplatesSeeders

app = FastAPI()
app.include_router(router=router)

@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with SessionLocal() as session:
        await TemplatesSeeders.run_seeders(session)


if __name__ == "__main__":
    uvicorn.run("main:app",host="localhost", port=8000, reload=True)