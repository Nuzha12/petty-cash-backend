from fastapi import FastAPI
from app.database import Base, engine

from app.models.company import Company
from app.routers import company

app = FastAPI(title="Petty Cash Management System API")

Base.metadata.create_all(bind=engine)

app.include_router(company.router)

@app.get("/")
def root():
    return {"message": "Petty Cash Backend Running"}

