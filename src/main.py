from fastapi import FastAPI, Depends
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

# Import exclusively from your clean async layer
from src.db.session import get_db
from src.auth.auth_router import router as auth_router
from src.orders.orders_router import router as orders_router

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

# Converted completely to non-blocking async execution
@app.get("/db-test")
async def test_db_connection(db: AsyncSession = Depends(get_db)):
    try:
        # Awaiting the execution forces it to use the asyncpg driver!
        await db.execute(text("SELECT 1"))
        return {"status": "success", "message": "Successfully connected to the Docker PostgreSQL database asynchronously!"}
    except Exception as e:
        return {"status": "error", "message": f"Database connection failed: {str(e)}"}