from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

from src.auth.auth_router import router as auth_router

app = FastAPI(
    title="ChopNow-API",
    version="1.0.0",
    description="A food delivery service that utilises all the complex features",
)

# Include the authentication router in the main application loop
app.include_router(auth_router)
@app.get("/")
async def root():
    return {
        "message": "Hello Welcome to ChopNow-API",
    }

@app.get("/greet/")
async def greet( name: Optional[str] = "User" ,title : str ="George") -> dict:
    return {
        "message": f"Hello {name}!",
        "title": title,
    }
        