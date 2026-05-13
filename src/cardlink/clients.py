import httpx
from typing import Optional

from controllers import (
    BalanceController,
    BillController,
    PayoutController,
    RefundController,
    PaymentController,
    SyncBillController,
    SyncPayoutController,
    SyncRefundController,
    SyncBalanceController,
    SyncPaymentController
)


class CardLinkAsyncClient:
    """
    Асинхронный клиент API CardLink.
    
    Клиент можно инициализировать один раз и использовать многократно.
    
    Примеры использования:
        
        from cadlink import CardLinkAsyncClient

        client = CardLinkAsyncClient(api_key="your_key")    
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
    
    async def _initialize(self) -> None:
        """Инициализация HTTP сессии
        
        Вызывается автоматически при использовании контекстного менеджера
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
            await self._initialize()
        
        try:
            response = await self._session.request(method, path, **kwargs)  # type: ignore
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"API Error {e.response.status_code}: {e.response.text}") from e
        except httpx.RequestError as e:
            raise ConnectionError(f"Network Error: {str(e)}") from e
        finally:
            await self._session.aclose()


class CardLinkSyncClient:
    """
    Синхронный клиент API CardLink.
    
    Клиент можно инициализировать один раз и использовать многократно.
    
    Примеры использования:
    
        from cardlink import CardLinkSyncClient
    
        client = CardLinkSyncClient(api_key="your_key")
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
        finally:
            self._session.close()
