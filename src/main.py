from fastapi import FastAPI

app = FastAPI(
    title="ChopNow-API",
    description="Production-ready, asynchronous food delivery backend gateway",
    version="1.0.0"
)

@app.get("/") #the route for the home/root path
async def read_root():
    return {"status": "healthy",
        "service": "ChopNow-API Core Engine",
        "docs_url": "/docs"
            }

@app.get("/greet/{name}")
async def greet(name: str) -> dict:
    return {"message": f"Hello, {name.upper()}!"}