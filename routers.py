from fastapi import APIRouter

router = APIRouter(prefix='/converter')

@router.get("/{from_currency}")
def converter(from_currency: str, to_currency:str, price:float):
    return {"msg": f"{from_currency}"}