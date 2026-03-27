from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine

from app.routers import company, manager, auth, category, budget, expense, report, receipt_router, dashboard_router

app = FastAPI(title="Petty Cash Management System API")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(company.router)
app.include_router(manager.router)
app.include_router(category.router)
app.include_router(budget.router)
app.include_router(expense.router)
app.include_router(report.router)
app.include_router(receipt_router.router)
app.include_router(dashboard_router.router)

app.mount("/uploads", StaticFiles(directory= "uploads"), name= "uploads")

@app.get("/")
def root():
    return {"message": "Petty Cash Backend Running"}

