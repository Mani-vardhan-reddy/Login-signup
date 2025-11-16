from app.database.database import Base, engine, SessionLocal
from fastapi import FastAPI
import uvicorn
import asyncio
from app.routes.signup_routes import router
from app.notifications_trmplates.templates_seeders_data import TemplatesSeeders
from app.kafka_service.kafka import kafka_service

app = FastAPI()
app.include_router(router=router)

@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with SessionLocal() as session:
        await TemplatesSeeders.run_seeders(session)
        
    asyncio.create_task(kafka_service.consume_message("email-topic"))

if __name__ == "__main__":
    uvicorn.run("main:app",host="localhost", port=8000, reload=True)