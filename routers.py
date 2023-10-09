from fastapi import APIRouter, status

router = APIRouter(prefix='/converter')

@router.get("/{from_currency}", status_code= status.HTTP_200_OK)
def converter(from_currency: str, to_currency:str, price:float):
    return {"msg": f"{from_currency}"}