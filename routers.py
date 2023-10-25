from asyncio import gather
from typing import List

from fastapi import APIRouter, Path, status

from converter import async_converter, sync_converter
from schemas import ConverterInput, ConverterOutput

router = APIRouter(prefix="/converter")


@router.get("/{from_currancy}", status_code=status.HTTP_200_OK)
def convert(
    from_currency: str,
    to_currency: str,
    price: float,
):
    to_currencies: List[str] = to_currency.split(",")
    result: List[float] = [
        sync_converter(from_currency, currency, price)
        for currency in to_currencies
    ]

    return result


@router.get("/async/{from_currancy}", status_code=status.HTTP_200_OK)
async def async_converter_router(
    from_currency: str,
    to_currency: str,
    price: float,
):
    to_currencies: List[str] = to_currency.split(",")
    result: List[float] = await gather(
        *[
            async_converter(from_currency, currency, price)
            for currency in to_currencies
        ]
    )

    return result


@router.get(
    "/async/v2/{from_currency}",
    status_code=status.HTTP_200_OK,
    response_model=ConverterOutput,
)
async def converter(
    body: ConverterInput,
    from_currency: str = Path(max_length=50, regex="^[A-Z]{3}$"),
):
    to_currencies: List[str] = body.to_currencies
    price = body.price
    result = await gather(
        *[
            async_converter(from_currency, currency, price)
            for currency in to_currencies
        ]
    )
    return ConverterOutput(
        response_msg="Successfully converted", converted_prices=result
    )
