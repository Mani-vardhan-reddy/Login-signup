from app.database.database import Base, engine
from fastapi import FastAPI
import uvicorn
from app.routes.signup_routes import router

app = FastAPI()
app.include_router(router=router)

@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    uvicorn.run("main:app",host="localhost", port=8000, reload=True)