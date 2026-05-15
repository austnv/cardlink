from httpx import Response

from .models.requests import (
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
    RefundFullCreateResponse,
    RefundPartialCreateRequest,
    RefundPartialCreateResponse,
    RefundSearchRequest,
    RefundSearchResponse,
    RefundStatusRequest,
    RefundStatusResponse,
)

class BaseSyncClient:
    """Абстрактный класс для синхронных клиентов"""
    def __init__(self, api_key: str, base_url: str):
        pass

    def _request(self, method: str, path: str, **kwargs) -> Response:
        pass


class BaseAsyncClient:
    """Абстрактный класс для асинхронных клиентов"""
    def __init__(self, api_key: str, base_url: str):
        pass

    async def _request(self, method: str, path: str, **kwargs) -> Response:
        pass


class BaseAsyncAPIController:
    """Базовый класс для всех контроллеров API"""
    def __init__(self, client: BaseAsyncClient):
        self.client = client


class BaseSyncAPIController:
    """Базовый класс для всех контроллеров API"""
    def __init__(self, client: BaseSyncClient):
        self.client = client


# Асинхронные контроллеры
class BillController(BaseAsyncAPIController):
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


class PaymentController(BaseAsyncAPIController):
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


class BalanceController(BaseAsyncAPIController):
    """Контроллер для работы с балансом (Balance)"""
    
    async def balance(self) -> MerchantBalanceResponse:
        """Получение баланса мерчанта
        
        Returns:
            MerchantBalanceResponse: Информация о балансах
        """
        response = await self.client._request("GET", "/merchant/balance")
        return MerchantBalanceResponse.model_validate(response.json())


class PayoutController(BaseAsyncAPIController):
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


class RefundController(BaseAsyncAPIController):
    """Контроллер для работы с возвратами (Refund)"""
    
    async def full_create(self, data: RefundFullCreateRequest) -> RefundFullCreateResponse:
        """Сделать полный возврат средств"""
        response = await self.client._request("POST", "/refund/full/create", json=data.model_dump(exclude_none=True))
        return RefundFullCreateResponse.model_validate(response.json())
    
    async def partial_create(self, data: RefundPartialCreateRequest) -> RefundPartialCreateResponse:
        """Сделать частичный возврат средств"""
        response = await self.client._request("POST", "/refund/partial/create", json=data.model_dump(exclude_none=True))
        return RefundPartialCreateResponse.model_validate(response.json())
    
    async def search(self, data: RefundSearchRequest) -> RefundSearchResponse:
        """Получить возвраты"""
        params = data.model_dump(exclude_none=True)
        response = await self.client._request("GET", "/refund/search", params=params)
        return RefundSearchResponse.model_validate(response.json())
    
    async def status(self, data: RefundStatusRequest) -> RefundStatusResponse:
        """Получить статус возврата"""
        params = data.model_dump(exclude_none=True)
        response = await self.client._request("GET", "/refund/status", params=params)
        return RefundStatusResponse.model_validate(response.json())


# Синхронные контроллеры
class SyncBillController(BaseSyncAPIController):
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


class SyncPaymentController(BaseSyncAPIController):
    """Синхронный контроллер для работы с платежами"""
    
    def search(self, data: PaymentSearchRequest) -> PaymentSearchResponse:
        params = data.model_dump(exclude_none=True)
        response = self.client._request("GET", "/payment/search", params=params)
        return PaymentSearchResponse.model_validate(response.json())

    def status(self, data: PaymentStatusRequest) -> PaymentStatusResponse:
        params = {k: v for k, v in data.model_dump(exclude_none=True).items()}
        response = self.client._request("GET", "/payment/status", params=params)
        return PaymentStatusResponse.model_validate(response.json())


class SyncBalanceController(BaseSyncAPIController):
    """Синхронный контроллер для работы с балансом"""
    
    def balance(self) -> MerchantBalanceResponse:
        response = self.client._request("GET", "/merchant/balance")
        return MerchantBalanceResponse.model_validate(response.json())


class SyncPayoutController(BaseSyncAPIController):
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


class SyncRefundController(BaseSyncAPIController):
    """Синхронный контроллер для работы с возвратами"""
    
    def full_create(self, data: RefundFullCreateRequest) -> RefundFullCreateResponse:
        """Сделать полный возврат средств"""
        response = self.client._request("POST", "/refund/full/create", json=data.model_dump(exclude_none=True))
        return RefundFullCreateResponse.model_validate(response.json())
    
    def partial_create(self, data: RefundPartialCreateRequest) -> RefundPartialCreateResponse:
        """Сделать частичный возврат средств"""
        response = self.client._request("POST", "/refund/partial/create", json=data.model_dump(exclude_none=True))
        return RefundPartialCreateResponse.model_validate(response.json())
    
    def search(self, data: RefundSearchRequest) -> RefundSearchResponse:
        params = data.model_dump(exclude_none=True)
        response = self.client._request("GET", "/refund/search", params=params)
        return RefundSearchResponse.model_validate(response.json())
    
    def status(self, data: RefundStatusRequest) -> RefundStatusResponse:
        params = data.model_dump(exclude_none=True)
        response = self.client._request("GET", "/refund/status", params=params)
        return RefundStatusResponse.model_validate(response.json())