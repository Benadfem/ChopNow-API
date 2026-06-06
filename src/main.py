from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI(
    title="ChopNow-API",
    version="1.0.0",
    description="A food delivery service that utilises all the complex features",
)

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
# let's create the model for the user through pydantic
class User(BaseModel):
    name: str
    age: int
    role: str
    is_active: bool


# let's create a user for the app
@app.post("/user")
# you create a variable of the User type
async def create_user(user: User):
    return {
        "name": user.name,
        "age": user.age,
        "role": user.role,
        "is_active": user.is_active
    }