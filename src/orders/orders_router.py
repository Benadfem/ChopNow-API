from fastapi import APIRouter

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

#lets create an endpoint for the router
@router.get("/orders")
async def orders() -> dict :
    return {
        "Message": "Wait! Orders will soon be created "
}