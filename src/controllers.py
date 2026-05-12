import httpx
from typing import Any, Dict, Optional, List
from pydantic import BaseModel

# Импорты из ваших файлов
from src.models.requests import (
    BillCreateRequest, BillCreateResponse,
    BillToggleActivityRequest, BillToggleActivityResponse,
    BillPaymentsRequest, BillPaymentResponse,
    BillSearchRequest, BillSearchResponse,
    BillStatusRequest, BillStatusResponse,
    PaymentSearchRequest, PaymentSearchResponse,
    PaymentStatusRequest, PaymentStatusResponse,
    MerchantBalanceResponse,
    PayoutPersonalCreateRequest,
    PayoutPersonalCreateResponse,
    PayoutRegularCreateRequest,
    PayoutRegularCreateResponse,
    PayoutSearchRequest,
    PayoutSearchResponse,
    PayoutStatusRequest,
    PayoutStatusResponse,
    PayoutSPBBanksResponse,
    RefundFullCreateRequest,
    RefundPartialCreateRequest,
    RefundSearchRequest,
    RefundSearchResponse,
    RefundStatusRequest,
    RefundStatusResponse,
)
from src.models.data import Payout


class BaseAPIController:
    """Базовый класс для всех контроллеров API"""
    def __init__(self, client):
        self.client = client


class BillController(BaseAPIController):
    """Контроллер для работы со счетами (Bill)"""
    
    async def create(self, data: BillCreateRequest) -> BillCreateResponse:
        """Создание счета на оплату
        
        Args:
            data: Параметры создания счета
            
        Returns:
            BillCreateResponse: Ответ с ссылкой на оплату
        """
        response = await self.client._request("POST", "/bill/create", json=data.model_dump(exclude_none=True))
        return BillCreateResponse.model_validate(response.json())

    async def toggle_activity(self, data: BillToggleActivityRequest) -> BillToggleActivityResponse:
        """Активация/деактивация счета
        
        Args:
            data: ID счета и статус активности
            
        Returns:
            BillToggleActivityResponse: Обновленный счет
        """
        response = await self.client._request(
            "POST", "/bill/toggle_activity", 
            json=data.model_dump(exclude_none=True)
        )
        return BillToggleActivityResponse.model_validate(response.json())

    async def payments(self, data: BillPaymentsRequest) -> BillPaymentResponse:
        """Список платежей по счету
        
        Args:
            data: ID счета и параметры пагинации
            
        Returns:
            BillPaymentResponse: Список платежей
        """
        params = {k: v for k, v in data.model_dump(exclude_none=True).items()}
        response = await self.client._request("GET", "/bill/payments", params=params)
        return BillPaymentResponse.model_validate(response.json())

    async def search(self, data: BillSearchRequest) -> BillSearchResponse:
        """Поиск счетов по критериям
        
        Args:
            data: Параметры поиска (даты, shop_id, пагинация)
            
        Returns:
            BillSearchResponse: Список счетов
        """
        params = data.model_dump(exclude_none=True)
        response = await self.client._request("GET", "/bill/search", params=params)
        return BillSearchResponse.model_validate(response.json())

    async def status(self, data: BillStatusRequest) -> BillStatusResponse:
        """Получение статуса счета
        
        Args:
            data: ID счета
            
        Returns:
            BillStatusResponse: Информация о счете
        """
        params = data.model_dump(exclude_none=True)
        response = await self.client._request("GET", "/bill/status", params=params)
        return BillStatusResponse.model_validate(response.json())


class PaymentController(BaseAPIController):
    """Контроллер для работы с платежами (Payment)"""
    
    async def search(self, data: PaymentSearchRequest) -> PaymentSearchResponse:
        """Поиск платежей по критериям
        
        Args:
            data: Параметры поиска (даты, shop_id, пагинация)
            
        Returns:
            PaymentSearchResponse: Список платежей
        """
        params = data.model_dump(exclude_none=True)
        response = await self.client._request("GET", "/payment/search", params=params)
        return PaymentSearchResponse.model_validate(response.json())

    async def status(self, data: PaymentStatusRequest) -> PaymentStatusResponse:
        """Получение статуса платежа
        
        Args:
            data: ID платежа и опционально флаги refunds/chargeback
            
        Returns:
            PaymentStatusResponse: Информация о платеже
        """
        params = {k: v for k, v in data.model_dump(exclude_none=True).items()}
        response = await self.client._request("GET", "/payment/status", params=params)
        return PaymentStatusResponse.model_validate(response.json())


class BalanceController(BaseAPIController):
    """Контроллер для работы с балансом (Balance)"""
    
    async def balance(self) -> MerchantBalanceResponse:
        """Получение баланса мерчанта
        
        Returns:
            MerchantBalanceResponse: Информация о балансах
        """
        response = await self.client._request("GET", "/merchant/balance")
        return MerchantBalanceResponse.model_validate(response.json())


class PayoutController(BaseAPIController):
    """Контроллер для работы с выплатами (Payout)"""
    
    async def create_personal(self, data: PayoutPersonalCreateRequest) -> PayoutPersonalCreateResponse:
        """Создать выплату на привязанный платежный аккаунт
        
        Args:
            data: Параметры выплаты
            
        Returns:
            PayoutPersonalCreateResponse: Информация о выплате
        """
        response = await self.client._request("POST", "/payout/personal/create", json=data.model_dump(exclude_none=True))
        return PayoutPersonalCreateResponse.model_validate(response.json())
    
    async def regular_create(self, data: PayoutRegularCreateRequest) -> PayoutRegularCreateResponse:
        """Отправить средства на указанные реквизиты
        
        Args:
            data: Параметры выплаты
            
        Returns:
            PayoutRegularCreateResponse: Информация о выплате
        """
        response = await self.client._request("POST", "/payout/regular/create", json=data.model_dump(exclude_none=True))
        return PayoutRegularCreateResponse.model_validate(response.json())
    
    async def search(self, data: PayoutSearchRequest) -> PayoutSearchResponse:
        """Получить выплаты
        
        Args:
            data: Параметры поиска (даты, пагинация)
            
        Returns:
            PayoutSearchResponse: Список выплат
        """
        params = data.model_dump(exclude_none=True)
        response = await self.client._request("GET", "/payout/search", params=params)
        return PayoutSearchResponse.model_validate(response.json())

    async def status(self, data: PayoutStatusRequest) -> PayoutStatusResponse:
        """Получить статус выплаты
        
        Args:
            data: ID выплаты или order_id
            
        Returns:
            PayoutStatusResponse: Информация о выплате
        """
        params = {k: v for k, v in data.model_dump(exclude_none=True).items()}
        response = await self.client._request("GET", "/payout/status", params=params)
        return PayoutStatusResponse.model_validate(response.json())
    
    async def spb_banks(self) -> PayoutSPBBanksResponse:
        """Получить список банков, доступных для СБП выплат
        
        Returns:
            PayoutSPBBanksResponse: Список банков
        """
        response = await self.client._request("GET", "/payout/dictionaries/sbp_banks")
        return PayoutSPBBanksResponse.model_validate(response.json())


class RefundController(BaseAPIController):
    """Контроллер для работы с возвратами (Refund)"""
    
    async def full_create(self, payment_id: str) -> RefundStatusResponse:
        """Сделать полный возврат средств
        
        Args:
            payment_id: ID платежа
            
        Returns:
            RefundStatusResponse: Информация о возврате
        """
        response = await self.client._request("POST", "/refund/full/create", json={"payment_id": payment_id})
        return RefundStatusResponse.model_validate(response.json())
    
    async def partial_create(self, payment_id: str, amount: float) -> RefundStatusResponse:
        """Сделать частичный возврат средств
        
        Args:
            payment_id: ID платежа
            amount: Сумма возврата
            
        Returns:
            RefundStatusResponse: Информация о возврате
        """
        response = await self.client._request(
            "POST", 
            "/refund/partial/create", 
            json={"payment_id": payment_id, "amount": amount}
        )
        return RefundStatusResponse.model_validate(response.json())
    
    async def search(self, data: RefundSearchRequest) -> RefundSearchResponse:
        """Получить возвраты
        
        Args:
            data: Параметры поиска
            
        Returns:
            RefundSearchResponse: Список возвратов
        """
        params = data.model_dump(exclude_none=True)
        response = await self.client._request("GET", "/refund/search", params=params)
        return RefundSearchResponse.model_validate(response.json())
    
    async def status(self, data: RefundStatusRequest) -> RefundStatusResponse:
        """Получить статус возврата
        
        Args:
            data: ID возврата
            
        Returns:
            RefundStatusResponse: Информация о возврате
        """
        params = data.model_dump(exclude_none=True)
        response = await self.client._request("GET", "/refund/status", params=params)
        return RefundStatusResponse.model_validate(response.json())


class CardLinkAsyncClient:
    """
    Асинхронный клиент API CardLink.
    
    Клиент можно инициализировать один раз и использовать многократно,
    либо использовать как контекстный менеджер.
    
    Примеры использования:
    
        # Вариант 1: Инициализация и ручное закрытие
        client = CardLinkAsyncClient(api_key="your_key")
        await client.initialize()
        
        bill = await client.bill.create(BillCreateRequest(amount=100.0, shop_id="shop_123"))
        
        await client.close()
        
        # Вариант 2: Контекстный менеджер (рекомендуется)
        async with CardLinkAsyncClient(api_key="your_key") as client:
            bill = await client.bill.create(BillCreateRequest(amount=100.0, shop_id="shop_123"))
    """
    
    def __init__(self, api_key: str, base_url: str = "https://cardlink.link/api/v1"):
        """Инициализация клиента
        
        Args:
            api_key: API ключ для авторизации
            base_url: Базовый URL API (по умолчанию https://cardlink.link/api/v1)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self._session: Optional[httpx.AsyncClient] = None
        
        # Подключение контроллеров
        self.bill = BillController(self)
        self.payment = PaymentController(self)
        self.balance = BalanceController(self)
        self.payout = PayoutController(self)
        self.refund = RefundController(self)
    
    async def initialize(self) -> None:
        """Инициализация HTTP сессии
        
        Вызывается автоматически при использовании контекстного менеджера
        или может быть вызвана явно перед первым запросом.
        """
        if self._session is None:
            self._session = httpx.AsyncClient(
                base_url=self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                timeout=30.0
            )
    
    async def _request(self, method: str, path: str, **kwargs) -> httpx.Response:
        """Внутренний метод выполнения HTTP-запросов
        
        Args:
            method: HTTP метод (GET, POST, etc.)
            path: Путь к эндпоинту
            **kwargs: Дополнительные аргументы для httpx
            
        Returns:
            httpx.Response: Ответ сервера
            
        Raises:
            RuntimeError: При ошибке API
            ConnectionError: При ошибке сети
        """
        if self._session is None:
            await self.initialize()
        
        try:
            response = await self._session.request(method, path, **kwargs)  # type: ignore
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"API Error {e.response.status_code}: {e.response.text}") from e
        except httpx.RequestError as e:
            raise ConnectionError(f"Network Error: {str(e)}") from e
    
    async def close(self) -> None:
        """Закрытие HTTP сессии"""
        if self._session:
            await self._session.aclose()
            self._session = None
    
    async def __aenter__(self):
        """Вход в контекстный менеджер"""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Выход из контекстного менеджера"""
        await self.close()


class CardLinkSyncClient:
    """
    Синхронный клиент API CardLink.
    
    Клиент можно инициализировать один раз и использовать многократно,
    либо использовать как контекстный менеджер.
    
    Примеры использования:
    
        # Вариант 1: Инициализация и ручное закрытие
        client = CardLinkSyncClient(api_key="your_key")
        
        bill = client.bill.create(BillCreateRequest(amount=100.0, shop_id="shop_123"))
        
        client.close()
        
        # Вариант 2: Контекстный менеджер (рекомендуется)
        with CardLinkSyncClient(api_key="your_key") as client:
            bill = client.bill.create(BillCreateRequest(amount=100.0, shop_id="shop_123"))
    """
    
    def __init__(self, api_key: str, base_url: str = "https://cardlink.link/api/v1"):
        """Инициализация клиента
        
        Args:
            api_key: API ключ для авторизации
            base_url: Базовый URL API (по умолчанию https://cardlink.link/api/v1)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self._session: Optional[httpx.Client] = None
        
        # Подключение контроллеров
        self.bill = SyncBillController(self)
        self.payment = SyncPaymentController(self)
        self.balance = SyncBalanceController(self)
        self.payout = SyncPayoutController(self)
        self.refund = SyncRefundController(self)
    
    def _get_session(self) -> httpx.Client:
        """Получение или создание HTTP сессии"""
        if self._session is None:
            self._session = httpx.Client(
                base_url=self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                timeout=30.0
            )
        return self._session
    
    def _request(self, method: str, path: str, **kwargs) -> httpx.Response:
        """Внутренний метод выполнения HTTP-запросов
        
        Args:
            method: HTTP метод (GET, POST, etc.)
            path: Путь к эндпоинту
            **kwargs: Дополнительные аргументы для httpx
            
        Returns:
            httpx.Response: Ответ сервера
            
        Raises:
            RuntimeError: При ошибке API
            ConnectionError: При ошибке сети
        """
        session = self._get_session()
        try:
            response = session.request(method, path, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"API Error {e.response.status_code}: {e.response.text}") from e
        except httpx.RequestError as e:
            raise ConnectionError(f"Network Error: {str(e)}") from e
    
    def close(self) -> None:
        """Закрытие HTTP сессии"""
        if self._session:
            self._session.close()
            self._session = None
    
    def __enter__(self):
        """Вход в контекстный менеджер"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Выход из контекстного менеджера"""
        self.close()


# Синхронные контроллеры
class SyncBillController(BillController):
    """Синхронный контроллер для работы со счетами"""
    
    def create(self, data: BillCreateRequest) -> BillCreateResponse:
        response = self.client._request("POST", "/bill/create", json=data.model_dump(exclude_none=True))
        return BillCreateResponse.model_validate(response.json())

    def toggle_activity(self, data: BillToggleActivityRequest) -> BillToggleActivityResponse:
        response = self.client._request("POST", "/bill/toggle_activity", json=data.model_dump(exclude_none=True))
        return BillToggleActivityResponse.model_validate(response.json())

    def payments(self, data: BillPaymentsRequest) -> BillPaymentResponse:
        params = {k: v for k, v in data.model_dump(exclude_none=True).items()}
        response = self.client._request("GET", "/bill/payments", params=params)
        return BillPaymentResponse.model_validate(response.json())

    def search(self, data: BillSearchRequest) -> BillSearchResponse:
        params = data.model_dump(exclude_none=True)
        response = self.client._request("GET", "/bill/search", params=params)
        return BillSearchResponse.model_validate(response.json())

    def status(self, data: BillStatusRequest) -> BillStatusResponse:
        params = data.model_dump(exclude_none=True)
        response = self.client._request("GET", "/bill/status", params=params)
        return BillStatusResponse.model_validate(response.json())


class SyncPaymentController(PaymentController):
    """Синхронный контроллер для работы с платежами"""
    
    def search(self, data: PaymentSearchRequest) -> PaymentSearchResponse:
        params = data.model_dump(exclude_none=True)
        response = self.client._request("GET", "/payment/search", params=params)
        return PaymentSearchResponse.model_validate(response.json())

    def status(self, data: PaymentStatusRequest) -> PaymentStatusResponse:
        params = {k: v for k, v in data.model_dump(exclude_none=True).items()}
        response = self.client._request("GET", "/payment/status", params=params)
        return PaymentStatusResponse.model_validate(response.json())


class SyncBalanceController(BalanceController):
    """Синхронный контроллер для работы с балансом"""
    
    def balance(self) -> MerchantBalanceResponse:
        response = self.client._request("GET", "/merchant/balance")
        return MerchantBalanceResponse.model_validate(response.json())


class SyncPayoutController(PayoutController):
    """Синхронный контроллер для работы с выплатами"""
    
    def create_personal(self, data: PayoutPersonalCreateRequest) -> PayoutPersonalCreateResponse:
        response = self.client._request("POST", "/payout/personal/create", json=data.model_dump(exclude_none=True))
        return PayoutPersonalCreateResponse.model_validate(response.json())
    
    def regular_create(self, data: PayoutRegularCreateRequest) -> PayoutRegularCreateResponse:
        response = self.client._request("POST", "/payout/regular/create", json=data.model_dump(exclude_none=True))
        return PayoutRegularCreateResponse.model_validate(response.json())
    
    def search(self, data: PayoutSearchRequest) -> PayoutSearchResponse:
        params = data.model_dump(exclude_none=True)
        response = self.client._request("GET", "/payout/search", params=params)
        return PayoutSearchResponse.model_validate(response.json())

    def status(self, data: PayoutStatusRequest) -> PayoutStatusResponse:
        params = {k: v for k, v in data.model_dump(exclude_none=True).items()}
        response = self.client._request("GET", "/payout/status", params=params)
        return PayoutStatusResponse.model_validate(response.json())
    
    def spb_banks(self) -> PayoutSPBBanksResponse:
        response = self.client._request("GET", "/payout/dictionaries/sbp_banks")
        return PayoutSPBBanksResponse.model_validate(response.json())


class SyncRefundController(RefundController):
    """Синхронный контроллер для работы с возвратами"""
    
    def full_create(self, payment_id: str) -> RefundStatusResponse:
        response = self.client._request("POST", "/refund/full/create", json={"payment_id": payment_id})
        return RefundStatusResponse.model_validate(response.json())
    
    def partial_create(self, payment_id: str, amount: float) -> RefundStatusResponse:
        response = self.client._request("POST", "/refund/partial/create", json={"payment_id": payment_id, "amount": amount})
        return RefundStatusResponse.model_validate(response.json())
    
    def search(self, data: RefundSearchRequest) -> RefundSearchResponse:
        params = data.model_dump(exclude_none=True)
        response = self.client._request("GET", "/refund/search", params=params)
        return RefundSearchResponse.model_validate(response.json())
    
    def status(self, data: RefundStatusRequest) -> RefundStatusResponse:
        params = data.model_dump(exclude_none=True)
        response = self.client._request("GET", "/refund/status", params=params)
        return RefundStatusResponse.model_validate(response.json())