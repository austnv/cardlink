"""
CardLink API Client - Асинхронный и синхронный клиент для [CardLink API](https://cardlink.link/reference/api)

Примеры использования:

    # Асинхронный клиент (рекомендуется)
    from pycadlink import CardLinkAsyncClient
    from pycadlink.models.requests import BillCreateRequest
    
    async def main():
        client = CardLinkAsyncClient(api_key="your_api_key")
        
        bill = await client.bill.create(BillCreateRequest(amount=100.0, shop_id="shop_123"))
    

    # Синхронный клиент
    from pycadlink import CardLinkSyncClient
    
    client = CardLinkSyncClient(api_key="your_api_key")
    bill = client.bill.create(BillCreateRequest(amount=100.0, shop_id="shop_123"))
"""

from .clients import CardLinkAsyncClient, CardLinkSyncClient
from .models import requests, data, enums

__all__ = [
    "CardLinkAsyncClient",
    "CardLinkSyncClient",
    "requests",
    "data",
    "enums",
]
