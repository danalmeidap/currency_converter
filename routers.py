from asyncio import gather
from typing import List

from fastapi import APIRouter, status

from converter import async_converter, sync_converter

router = APIRouter(prefix="/converter")


@router.get("/{from_currancy}", status_code=status.HTTP_200_OK)
def converter(from_currency: str, to_currency: str, price: float):
    to_currencies: List[str] = to_currency.split(",")
    result: List[float] = [
        sync_converter(from_currency, currency, price)
        for currency in to_currencies
    ]

    return result


@router.get("/async/{from_currancy}", status_code=status.HTTP_200_OK)
async def async_converter_router(
    from_currency: str, to_currency: str, price: float
):
    to_currencies: List[str] = to_currency.split(",")
    result: List[float] = await gather(
        *[
            async_converter(from_currency, currency, price)
            for currency in to_currencies
        ]
    )

    return result
