from fastapi import APIRouter, status
from converter import sync_converter
from typing import List

router = APIRouter(prefix="/converter")

@router.get("/{from_currancy}", status_code= status.HTTP_200_OK)
def converter(from_curreacy: str, to_currency:str, price:float):
    to_currencies:List[str] = to_currency.split(',')
    result:List[float] = [sync_converter(from_curreacy, currency, price) for currency  in to_currencies] 

    return result
