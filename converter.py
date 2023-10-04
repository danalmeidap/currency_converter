from requests import get
from os import getenv
from fastapi import HTTPException, status
from config import settings

API_KEY = getenv("API_KEY")

def sync_converter(from_currency:str, to_currency:str, price:float):
    url = settings.api.url+f'from_currency={from_currency}&to_currency={to_currency}&apikey={API_KEY}'
    
    try:
        response = get(url)
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Internal error on alpha vantange requests: {error}')

    data = response.json()    

    if "Realtime Currency Exchange Rate" not in data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Probably invalid currencies given')
    
    return float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])