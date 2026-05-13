"""
CardLink API Client - Асинхронный и синхронный клиент для CardLink API

Примеры использования:

    # Асинхронный клиент (рекомендуется)
    from src import CardLinkAsyncClient
    from src.models.requests import BillCreateRequest
    
    async def main():
        client = CardLinkAsyncClient(api_key="your_api_key")
        
        bill = await client.bill.create(BillCreateRequest(amount=100.0, shop_id="shop_123"))
    

    # Синхронный клиент
    from src import CardLinkSyncClient
    
    client = CardLinkSyncClient(api_key="your_api_key")
    bill = client.bill.create(BillCreateRequest(amount=100.0, shop_id="shop_123"))
"""

from clients import CardLinkAsyncClient, CardLinkSyncClient
from models import requests, data, enums

__version__ = "0.1.0"
__author__ = "austnv"
__all__ = [
    "CardLinkAsyncClient",
    "CardLinkSyncClient",
    "requests",
    "data",
    "enums",
]