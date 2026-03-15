from fastapi import FastAPI
from app.database import Base, engine

from app.models.company import Company
from app.models.manager import Manager

from app.routers import company, manager, auth, category, budget

app = FastAPI(title="Petty Cash Management System API")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(company.router)
app.include_router(manager.router)
app.include_router(category.router)
app.include_router(budget.router)

@app.get("/")
def root():
    return {"message": "Petty Cash Backend Running"}

