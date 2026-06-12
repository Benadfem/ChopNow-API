from fastapi import APIRouter

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

#let's create an endpoint for the router
@router.get("/")
async def orders() -> dict :
    return {
        "Message": "Wait! Orders will soon be created "
}