from fastapi import FastAPI
from typing import Optional

app = FastAPI(
    title="ChopNow-API",
    version="1.0.0",
    description="A food delivery service that utilises all the complex features",
)

@app.get("/")
async def root():
    return {
        "message": "Hello World",
    }

@app.get("/greet/")
async def greet( name: Optional[str] = "User" ,title : str ="George") -> dict:
    return {
        "message": f"Hello {name}!",
        "title": title,
    }
