from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional
from datetime import datetime

from src.models.enums import (
    BillType,
    Locale,
    BillCurrency,
    PaymentMethod,
    BillStatus,
    PaymentStatus,
    PaymentCurrency,
    PayoutCurrency,
    PayoutAccountType,
    PayoutStatus,
    RefundStatus,
    RefundCurrency,
    EntityType,
)

from src.models.data import (
    RequestField,
    Item,
    Payment,
    PaginationLinks,
    PaginationMeta,
    Bill,
    Refund,
    Chargeback,
    Balance,
    Payout,
    SBPBank,
)

class BillCreateRequest(BaseModel):
    amount: Decimal = Field(description='Сумма счета на оплату')
    shop_id: str = Field(description='Уникальный идентификатор магазина, к которому относится платеж. Без этого параметра не будет работать Success URL, Fail URL и Result URL')
    order_id: Optional[str] = Field(description='Уникальный идентификатор заказа. Будет возвращен в postback.', default=None)
    description: Optional[str] = Field(description='Описание платежа', default=None)
    type: Optional[BillType] = Field(description='Тип платежа. Одноразовый или многоразовый. Если выбран одноразовый, то второй раз оплатить не получится.', default=None)
    locale: Optional[Locale] = Field(description='Локаль, язык в котором будет отображаться форма платежа', default=None)
    currency_in: Optional[BillCurrency] = Field(description='Валюта, в которой оплачивается счет. Если не передана, то используется валюта магазина. Если shop_id не определен, то используется RUB.', default=None)
    custom: Optional[str] = Field(description='Произвольное поле. Будет возвращено в postback.', default=None)
    payer_pays_commission: Optional[bool] = Field(description='Параметр, который указывает на то, кто будет оплачивать комиссию за входящий платёж.', default=None)
    payer_email: Optional[str] = Field(description='Параметр, который заполняет email клиента на платёжной странице.', default=None)
    name: Optional[str] = Field(description='Название ссылки. Укажите, за что принимаете средства. Этот текст будет отображен в платежной форме.', default=None)
    ttl: Optional[int] = Field(description='Время жизни счета на оплату в секундах.', default=None)
    return_url: Optional[str] = Field(description='URL для кнопки "Назад в магазин" на странице оплаты. Домен должен совпадать с тем, что указан при добавлении магазина в систему', default=None)
    success_url: Optional[str] = Field(description='Страница успешной оплаты.', default=None)
    fail_url: Optional[str] = Field(description='Страница неуспешной оплаты.', default=None)
    payment_method: Optional[PaymentMethod] = Field(description='Если указан этот параметр, то при переходе на платежную форму этот способ оплаты будет выбран автоматически, без возможности выбора другого способ оплаты.', default=None)
    request_fields: Optional[RequestField] = Field(default=None)
    items: Optional[list[Item]] = Field(description='Список товаров', default=None)


class BillCreateResponse(BaseModel):
    success: Optional[bool] = Field(description='Флаг успешности запроса', default=None)
    link_url: Optional[str] = Field(description='Ссылка на страницу с QR кодом', default=None)
    link_page_url: Optional[str] = Field(description='Ссылка на оплату', default=None)
    bill_id: Optional[str] = Field(description='Уникальный идентификатор счета', default=None)


class BillToggleActivityRequest(BaseModel):
    id: str = Field(description='Уникальный идентификатор счета')
    active: bool = Field(description='0 - деактивировать счет, 1 - активировать счет')


class BillToggleActivityResponse(BaseModel):
    id: Optional[str] = Field(description='Уникальный идентификатор счета', default=None)
    order_id: Optional[str] = Field(description='Уникальный идентификатор заказа на вашей стороне', default=None)
    active: Optional[bool] = Field(description='Флаг активности счета', default=None)
    status: Optional[BillStatus] = Field(description='Статус счета', default=None)
    amount: Optional[Decimal] = Field(description='Сумма, на которую выставлен счет', default=None)
    type: Optional[BillType] = Field(description='Тип счета', default=None)
    created_at: Optional[datetime] = Field(description='Дата и время создания счета', default=None)
    currency_in: Optional[BillCurrency] = Field(description='Валюта, в которой оплачивается счет', default=None)
    ttl: Optional[int] = Field(description='Время жизни счета на оплату в секундах.', default=None)
    success: Optional[bool] = Field(description='Флаг успешности запроса', default=None)


class BillPaymentsRequest(BaseModel):
    id: str = Field(description='Уникальный идентификатор счета')
    per_page: Optional[int] = Field(description='Количество элементов на странице', default=None)
    cursor: Optional[str] = Field(description='Указатель на страницу', default=None)


class BillPaymentResponse(BaseModel):
    success: Optional[bool] = Field(description='Флаг успешности запроса', default=None)
    data: Optional[list[Payment]] = Field(description='Массив платежей, относящихся к этому счету на оплату', default=None)
    links: Optional[list[PaginationLinks]] = Field(description='Ссылки для пагинации', default=None)
    meta: Optional[list[PaginationMeta]] = Field(description='Мета данные пагинации', default=None)


class BillSearchRequest(BaseModel):
    start_date: Optional[datetime] = Field(description='Начальная датавремя для получения счетов в UTC', default=None)
    finish_date: Optional[datetime] = Field(description='Конечная датавремя для получения счетов в UTC', default=None)
    shop_id: Optional[str] = Field(description='Уникальный идентификатор магазина', default=None)
    per_page: Optional[int] = Field(description='Количество элементов на странице', default=None)
    cursor: Optional[str] = Field(description='Указатель на страницу', default=None)


class BillSearchResponse(BaseModel):
    success: Optional[bool] = Field(description='Флаг успешности запроса', default=None)
    data: Optional[list[Bill]] = Field(description='Массив счетов она оплату, удовлетворяющих криетриям запроса', default=None)
    links: Optional[list[PaginationLinks]] = Field(description='Ссылки для пагинации', default=None)
    meta: Optional[list[PaginationMeta]] = Field(description='Мета данные пагинации', default=None)


class BillStatusRequest(BaseModel):
    id: str = Field(description='Уникальный идентификатор счета')


class BillStatusResponse(BaseModel):
    id: Optional[str] = Field(description='Уникальный идентификатор счета', default=None)
    order_id: Optional[str] = Field(description='Уникальный идентификатор заказа на вашей стороне', default=None)
    active: Optional[bool] = Field(description='Флаг активности счета', default=None)
    status: Optional[BillStatus] = Field(description='Статус счета', default=None)
    amount: Optional[Decimal] = Field(description='Сумма, на которую выставлен счет', default=None)
    type: Optional[BillType] = Field(description='Тип счета', default=None)
    created_at: Optional[datetime] = Field(description='Дата и время создания счета', default=None)
    currency_in: Optional[BillCurrency] = Field(description='Валюта, в которой оплачивается счет', default=None)
    ttl: Optional[int] = Field(description='Время жизни счета на оплату в секундах.', default=None)
    success: Optional[bool] = Field(description='Флаг успешности запроса', default=None)


class PaymentSearchRequest(BaseModel):
    start_date: Optional[datetime] = Field(description='Начальная датавремя для получения платежей в UTC', default=None)
    finish_date: Optional[datetime] = Field(description='Конечная датавремя для получения платежей в UTC', default=None)
    shop_id: Optional[str] = Field(description='Уникальный идентификатор магазина', default=None)
    per_page: Optional[int] = Field(description='Количество элементов на странице', default=None)
    cursor: Optional[str] = Field(description='Указатель на страницу', default=None)


class PaymentSearchResponse(BaseModel):
    success: Optional[bool] = Field(description='Флаг успешности запроса', default=None)
    data: Optional[list[Payment]] = Field(description='Информация о платежах', default=None)
    links: Optional[list[PaginationLinks]] = Field(description='Ссылки для пагинации', default=None)
    meta: Optional[list[PaginationMeta]] = Field(description='Мета данные пагинации', default=None)


class PaymentStatusRequest(BaseModel):
    id: str = Field(description='Уникальный идентификатор платежа')
    refunds: Optional[bool] = Field(description='Включить в ответ информацию по рефандам', default=None)
    chargeback: Optional[bool] = Field(description='Включить в ответ информацию по чарджбэкам', default=None)


class PaymentStatusResponse(BaseModel):
    id: Optional[str] = Field(description='Уникальный идентификатор платежа', default=None)
    bill_id: Optional[str] = Field(description='Уникальный идентификатор счета, которому принадлежит платеж', default=None)
    status: Optional[PaymentStatus] = Field(description='Статус платежа', default=None)
    amount: Optional[Decimal] = Field(description='Сумма платежа', default=None)
    commission: Optional[Decimal] = Field(description='Комиссия', default=None)
    account_amount: Optional[Decimal] = Field(description='Сумма зачисления на баланс', default=None)
    account_currency_code: Optional[str] = Field(description='Валюта зачисления на баланс', default=None)
    refunded_amount: Optional[Decimal] = Field(description='Сумма возвратов по платежу', default=None)
    from_card: Optional[str] = Field(description='Номер карты, с которой произошла оплата (При оплате банковской картой)', default=None)
    account_bank: Optional[str] = Field(description='Банк счета пользователя, с которого произошла оплата', default=None)
    currency_in: Optional[PaymentCurrency] = Field(description='Валюта, в которой оплачивается счет', default=None)
    created_at: Optional[datetime] = Field(description='Дата и время создания платежа', default=None)
    payer_phone: Optional[str] = Field(description='Телефон плательщика', default=None)
    payer_email: Optional[str] = Field(description='Почта плательщика', default=None)
    payer_name: Optional[str] = Field(description='Имя плательщика', default=None)
    payer_comment: Optional[str] = Field(description='Комментарий плательщика', default=None)
    error_code: Optional[int] = Field(description='Код ошибки', default=None)
    error_message: Optional[str] = Field(description='Описание ошибки', default=None)
    description: Optional[str] = Field(description='Описание', default=None)
    success: Optional[bool] = Field(description='Флаг успешности запроса', default=None)
    refunds: Optional[list[Refund]] = Field(description='Массив рефандов. Если был передан refunds=true', default=None)
    chargeback: Optional[list[Chargeback]] = Field(description='Чарджбек. Если существует и если был передан chargeback=true', default=None)


class MerchantBalanceResponse(BaseModel):
    balances: Optional[list[Balance]] = Field(description='Массив, содержащий информацию о балансах мерчанта', default=None)
    success: Optional[bool] = Field(description='Флаг успешности запроса', default=None)


class PayoutPersonalCreateRequest(BaseModel):
    amount: Decimal = Field(description='Сумма выплаты')
    payout_account_id: str = Field(description='Уникальный идентификатор платежного аккаунта, на который будет произведена выплата.')
    account_currency: Optional[PayoutCurrency] = Field(description='Валюта баланса, с которого необходимо списать средства за выплату.', default=None)
    recipient_pays_commission: Optional[bool] = Field(description='Параметр отвечающий за то, кто платит комиссию (true-комиссию платит получающий выплату, если false-то комиссия будет вычтена с баланса аккаунта)', default=None)
    order_id: Optional[str] = Field(description='Уникальный идентификатор заказа.', default=None)


class PayoutPersonalCreateResponse(BaseModel):
    data: Optional[list[Payout]] = Field(description='Информация о выплате', default=None)
    success: Optional[bool] = Field(description='Флаг успешности запроса', default=None)


class PayoutRegularCreateRequest(BaseModel):
    amount: Decimal = Field(description='Сумма выплаты')
    currency: PayoutCurrency = Field(description='Валюта')
    account_type: PayoutAccountType = Field(description='Тип аккаунта, на который отправляются средства')
    account_identifier: str = Field(description='Идентификатор аккаунта в зависимости от account_type: credit_card - номер карты, sbp - номер телефона, crypto - адрес кошелька, steam - логин пользователя в Steam')
    account_bank: str = Field(description='Member ID банка для account_type=sbp. Список доступных банков вы можете получить методом dictionary_spb_banks')
    card_holder: str = Field(description='Держатель карты для account_type=credit_card. Как указано на карте.')
    account_network: str = Field(description='Сеть для отправки криптовалюты/токенов для account_type=crypto. TRX - Tron сеть, ETH - Ethereum.')
    account_currency: Optional[PayoutAccountType] = Field(description='Валюта баланса', default=None)
    recipient_pays_commission: Optional[bool] = Field(description='Параметр отвечающий за то, кто платит комиссию (true - комиссию платит получающий выплату, если false - то комиссия будет вычтена с баланса аккаунта)', default=None)
    order_id: Optional[str] = Field(description='Уникальный идентификатор заказа.', default=None)


class PayoutRegularCreateResponse(BaseModel):
    data: Optional[list[Payout]] = Field(description='Информация о выплате', default=None)
    success: Optional[bool] = Field(description='Флаг успешности запроса', default=None)


class PayoutSearchRequest(BaseModel):
    start_date: Optional[datetime] = Field(description='Начальная датавремя для получения выплат в UTC', default=None)
    finish_date: Optional[datetime] = Field(description='Конечная датавремя для получения выплат в UTC', default=None)
    per_page: Optional[int] = Field(description='Количество элементов на странице', default=None)
    cursor: Optional[str] = Field(description='Указатель на страницу', default=None)


class PayoutSearchResponse(BaseModel):
    success: Optional[bool] = Field(description='Флаг успешности запроса', default=None)
    data: Optional[list[Payout]] = Field(description='Массив выплат', default=None)
    success: Optional[bool] = Field(description='', default=None)
    success: Optional[bool] = Field(description='', default=None)
    links: Optional[list[PaginationLinks]] = Field(description='Ссылки для пагинации', default=None)
    meta: Optional[list[PaginationMeta]] = Field(description='Мета данные пагинации', default=None)


class PayoutStatusRequest(BaseModel):
    id: Optional[str] = Field(description='Уникальный идентификатор выплаты. Обязателен, если не передан order_id', default=None)
    order_id: Optional[str] = Field(description='Уникальный идентификатор заказа. Обязателен, если не передан id', default=None)


class PayoutStatusResponse(BaseModel):
    id: Optional[str] = Field(description='Уникальный идентификатор выплаты', default=None)
    status: Optional[PayoutStatus] = Field(description='Статус выплаты', default=None)
    order_id: Optional[str] = Field(description='Уникальный идентификатор заказа', default=None)
    account_identifier: Optional[str] = Field(description='Платежный аккаунт, на который производится выплата', default=None)
    amount: Optional[Decimal] = Field(description='В случае recipient_pays_commission:false поле amount - сумма выплаты с учетом комиссии, в случае recipient_pays_commission:true поле amount - оригинальная сумма выплаты', default=None)
    account_amount: Optional[Decimal] = Field(description='Сумма, списанная с баланса', default=None)
    commission: Optional[Decimal] = Field(description='Комиссия сервиса', default=None)
    account_commission: Optional[Decimal] = Field(description='Комиссия сервиса в валюте баланса', default=None)
    currency: Optional[PayoutCurrency] = Field(description='Валюта выплаты', default=None)
    account_currency: Optional[PayoutCurrency] = Field(description='Валюта баланса', default=None)
    created_at: Optional[datetime] = Field(description='Дата и время создания выплаты', default=None)
    error_code: Optional[int] = Field(description='Код ошибки', default=None)
    error_message: Optional[int] = Field(description='Описание ошибки', default=None)
    success: Optional[bool] = Field(description='Флаг успешности запроса', default=None)


class PayoutSPBBanksResponse(BaseModel):
    data: Optional[list[SBPBank]] = Field(description='Массив банков', default=None)
    success: Optional[bool] = Field(description='Флаг успешности запроса', default=None)
    

# TODO: Refund, Postback

# =============================================================================
# Refund Models
# =============================================================================

class RefundFullCreateRequest(BaseModel):
    """Запрос на полный возврат средств"""
    payment_id: str = Field(description='Уникальный идентификатор платежа')


class RefundPartialCreateRequest(BaseModel):
    """Запрос на частичный возврат средств"""
    payment_id: str = Field(description='Уникальный идентификатор платежа')
    amount: Decimal = Field(description='Сумма возврата')


class RefundSearchRequest(BaseModel):
    """Запрос на поиск возвратов"""
    payment_id: Optional[str] = Field(description='ID платежа', default=None)
    per_page: Optional[int] = Field(description='Количество элементов на странице', default=None)
    cursor: Optional[str] = Field(description='Указатель на страницу', default=None)


class RefundSearchResponse(BaseModel):
    """Ответ на поиск возвратов"""
    success: Optional[bool] = Field(description='Флаг успешности запроса', default=None)
    data: Optional[list[Refund]] = Field(description='Массив возвратов', default=None)
    links: Optional[PaginationLinks] = Field(description='Ссылки для пагинации', default=None)
    meta: Optional[PaginationMeta] = Field(description='Мета данные пагинации', default=None)


class RefundStatusRequest(BaseModel):
    """Запрос на получение статуса возврата"""
    id: str = Field(description='Уникальный идентификатор возврата')


class RefundStatusResponse(BaseModel):
    """Ответ со статусом возврата"""
    id: Optional[str] = Field(description='Уникальный идентификатор возврата', default=None)
    status: Optional[RefundStatus] = Field(description='Статус возврата', default=None)
    amount: Optional[Decimal] = Field(description='Сумма возврата', default=None)
    currency: Optional[RefundCurrency] = Field(description='Валюта', default=None)
    entity_type: Optional[EntityType] = Field(description='Тип возврата', default=None)
    entity_id: Optional[str] = Field(description='Уникальный идентификатор платежа', default=None)
    created_at: Optional[datetime] = Field(description='Дата и время создания возврата', default=None)
    success: Optional[bool] = Field(description='Флаг успешности запроса', default=None)
