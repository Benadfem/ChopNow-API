from fastapi import FastAPI, Depends
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import text

# Corrected local imports based on main.py being inside the src/ directory
from database import get_db
from auth.auth_router import router as auth_router
from orders.orders_router import router as orders_router

app = FastAPI(
    title="ChopNow-API",
    version="1.0.0",
    description="A food delivery service that utilises all the complex features",
)

# Seamlessly include your modular feature routers
app.include_router(auth_router)
app.include_router(orders_router)

@app.get("/")
async def root():
    return {
        "message": "Hello Welcome to ChopNow-API",
    }

@app.get("/greet/")
async def greet(name: Optional[str] = "User", title: str = "George") -> dict:
    return {
        "message": f"Hello {name}!",
        "title": title,
    }

@app.get("/db-test")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Utilizing text() prevents modern SQLAlchemy execution errors
        db.execute(text("SELECT 1"))
        return {"status": "success", "message": "Successfully connected to the Docker PostgreSQL database!"}
    except Exception as e:
        return {"status": "error", "message": f"Database connection failed: {str(e)}"}