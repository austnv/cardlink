import httpx
from typing import Any, Dict, Optional, List
from pydantic import BaseModel

# Импорты из ваших файлов
from models.requests import (
    BillCreateRequest, BillCreateResponse,
    BillToggleActivityRequest, BillToggleActivityResponse,
    BillPaymentsRequest, BillPaymentResponse,
    BillSearchRequest, BillSearchResponse,
    BillStatusRequest, BillStatusResponse,
    PaymentSearchRequest, PaymentSearchResponse,
    PaymentStatusRequest, PaymentStatusResponse,
    MerchantBalanceResponse
)
from models.data import Payout


class BaseAPIController:
    """Базовый класс для всех контроллеров API"""
    def __init__(self, client: 'CardLinkClient'):
        self.client = client


class BillController(BaseAPIController):
    async def create(self, data: BillCreateRequest) -> BillCreateResponse:
        """Создание счета на оплату"""
        response = await self.client._request("POST", "/bill/create", json=data.model_dump(exclude_none=True))
        return BillCreateResponse.model_validate(response.json())

    async def toggle_activity(self, data: BillToggleActivityRequest) -> BillToggleActivityResponse:
        """Активация/деактивация счета"""
        response = await self.client._request(
            "POST", "/bill/toggle_activity", 
            json=data.model_dump(exclude_none=True)
        )
        return BillToggleActivityResponse.model_validate(response.json())

    async def payments(self, data: BillPaymentsRequest) -> BillPaymentResponse:
        """Список платежей по счету"""
        params = {k: v for k, v in data.model_dump(exclude_none=True).items()}
        response = await self.client._request("GET", "/bill/payments", params=params)
        return BillPaymentResponse.model_validate(response.json())

    async def search(self, data: BillSearchRequest) -> BillSearchResponse:
        """Поиск счетов по критериям"""
        params = data.model_dump(exclude_none=True)
        response = await self.client._request("GET", "/bill/search", params=params)
        return BillSearchResponse.model_validate(response.json())

    async def status(self, data: BillStatusRequest) -> BillStatusResponse:
        """Получение статуса счета"""
        params = data.model_dump(exclude_none=True)
        response = await self.client._request("GET", "/bill/status", params=params)
        return BillStatusResponse.model_validate(response.json())


class PaymentController(BaseAPIController):
    async def search(self, data: PaymentSearchRequest) -> PaymentSearchResponse:
        """Поиск платежей по критериям"""
        params = data.model_dump(exclude_none=True)
        response = await self.client._request("GET", "/payment/search", params=params)
        return PaymentSearchResponse.model_validate(response.json())

    async def status(self, data: PaymentStatusRequest) -> PaymentStatusResponse:
        """Получение статуса платежа"""
        params = {k: v for k, v in data.model_dump(exclude_none=True).items()}
        response = await self.client._request("GET", "/payment/status", params=params)
        return PaymentStatusResponse.model_validate(response.json())


class BalanceController(BaseAPIController):
    async def balance(self) -> MerchantBalanceResponse:
        """Получение баланса мерчанта"""
        response = await self.client._request("GET", "/merchant/balance")
        return MerchantBalanceResponse.model_validate(response.json())


class CardLinkClient:
    """
    Главный асинхронный клиент API CardLink.

    Использование:
    
        async with CardLinkAsyncClient(api_key="your_key") as client:
            bill = await client.bill.create(BillCreateRequest(amount=100.0, shop_id="shop_123"))
    """
    def __init__(self, api_key: str, base_url: str = "https://cardlink.link/api/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        
        # Асинхронная HTTP сессия
        self._session = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            timeout=30.0
        )

        # Подключение контроллеров
        self.bill = BillController(self)
        self.payment = PaymentController(self)
        self.balance = BalanceController(self)

    async def _request(self, method: str, path: str, **kwargs) -> httpx.Response:
        """Внутренний асинхронный метод выполнения HTTP-запросов"""
        try:
            response = await self._session.request(method, path, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            # Здесь можно добавить кастомную обработку ошибок API (парсинг JSON-ответа об ошибке)
            raise RuntimeError(f"API Error {e.response.status_code}: {e.response.text}") from e
        except httpx.RequestError as e:
            raise ConnectionError(f"Network Error: {str(e)}") from e

    async def aclose(self):
        """Закрытие асинхронной сессии"""
        await self._session.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()