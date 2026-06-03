from fastapi import FastAPI

app = FastAPI()

@app.get("/") #the route for the home/root path
async def read_root():
    return {"message": "Hello World"}

@app.get("/greet/{name}")
async def greet(name: str) -> dict:
    return {"message": f"Hello, {name.upper()}!"}