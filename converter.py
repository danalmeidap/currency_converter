from requests import get
from os import getenv
from fastapi import HTTPException, status
from config import settings
from aiohttp import ClientSession

API_KEY: str = getenv("API_KEY")


def sync_converter(from_currency: str, to_currency: str, price: float):
    url: str = (
        settings.api.url
        + f"from_currency={from_currency}&to_currency={to_currency}&apikey={API_KEY}"
    )

    try:
        response: str | bytes = get(url)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error on alpha vantange requests: {error}",
        )

    data: str | bytes = response.json()

    if "Realtime Currency Exchange Rate" not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Probably invalid currencies given",
        )

    exchange_rate: float = float(
        data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
    )

    return price * exchange_rate


async def async_converter(from_currency: str, to_currency: str, price: float):
    url: str = (
        settings.api.url
        + f"from_currency={from_currency}&to_currency={to_currency}&apikey={API_KEY}"
    )

    try:
        async with ClientSession() as session:
            async with session.get(url) as response:
                data: str | bytes = await response.json()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error on alpha vantange requests: {error}",
        )

    if "Realtime Currency Exchange Rate" not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Probably invalid currencies given",
        )

    exchange_rate: float = float(
        data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
    )

    return price * exchange_rate


