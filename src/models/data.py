"""
Pydantic models for the API
"""

from pydantic import BaseModel, Field, model_validator
from decimal import Decimal
from datetime import datetime
from typing import Optional, Any

from enums import (
    BillStatus,
    BillType,
    BillCurrency,
    PaymentStatus,
    PaymentCurrency,
    ChargebackStatus,
    _BalanceCurrency,
    PayoutCurrency,
    PayoutStatus,
    PayoutPostbackStatus,
    ChargebacPostbackStatus,
    EntityType,
    P2PDealCurrency,
    P2PDealPaymentCommissionApplyType,
    P2PDealPostbackStatus,
    PaymentPostbackAccountType,
    PayoutPostbackAccountType,
    PayoutPostbackCommissionApplyType,
    PayoutPostbackCurrency,
    RefundCurrency,
    RefundPostbackCurrency,
    RefundPostbackStatus,
    RefundStatus
)


# Модели данных

class Bill(BaseModel):
    id: Optional[str] = Field(description='Уникальный идентификатор счета', default=None)
    order_id: Optional[str] = Field(description='Уникальный идентификатор заказа на вашей стороне', default=None)
    active: Optional[bool] = Field(description='Флаг активности счета', default=None)
    status: Optional[BillStatus] = Field(description='Статус счета', default=None)
    amount: Optional[Decimal] = Field(description='Сумма, на которую выставлен счет', default=None)
    type: Optional[BillType] = Field(description='Тип счета', default=None)
    created_at: Optional[datetime] = Field(description='Дата и время создания счета', default=None)
    currency_in: Optional[BillCurrency] = Field(description='Валюта, в которой оплачивается счет', default=None)
    ttl: Optional[int] = Field(description='Время жизни счета на оплату в секундах.', default=None)


class Payment(BaseModel):
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
    payer_name: Optional[str] = Field(description='Комментарий плательщика', default=None)
    payer_comment: Optional[str] = Field(description='Телефон плательщика', default=None)
    error_code: Optional[int] = Field(description='Код ошибки', default=None)
    error_message: Optional[str] = Field(description='Описание ошибки', default=None)
    description: Optional[str] = Field(description='Описание', default=None)


class Chargeback(BaseModel):
    id: Optional[str] = Field(description='Чарджбэк ID', default=None)
    payment_id: Optional[str] = Field(description='ID Платежа', default=None)
    status: Optional[ChargebackStatus] = Field(description='Статус', default=None)
    created_at: Optional[datetime] = Field(description='Дата/время создания', default=None)


class Balance(BaseModel):
    currency: Optional[_BalanceCurrency] = Field(description='Валюта баланса', default=None)
    balance_available: Optional[Decimal] = Field(description='Доступный баланс', default=None)
    balance_locked: Optional[Decimal] = Field(description='Заблокированный баланс во время выплаты средств', default=None)
    balance_hold: Optional[Decimal] = Field(description='Временно удержанный баланс. Переходит в доступный спустя время', default=None)


class Payout(BaseModel):
    id: Optional[str] = Field(description='Уникальный идентификатор выплаты', default=None)
    status: Optional[PayoutStatus] = Field(description='Статус выплаты', default=None)
    order_id: Optional[str] = Field(description='Уникальный идентификатор заказа', default=None)
    account_identifier: Optional[str] = Field(description='Платежный аккаунт, на который производится выплата', default=None)
    amount: Optional[Decimal] = Field(description='В случае recipient_pays_commission:false поле amount - сумма выплаты с учетом комиссии, в случае recipient_pays_commission:true поле amount - оригинальная сумма выплаты', default=None)
    account_amount: Optional[Decimal] = Field(description='Сумма, списанная с баланса', default=None)
    commission: Optional[Decimal] = Field(description='Комиссия сервиса', default=None)
    account_commission: Optional[Decimal] = Field(description='Комиссия сервиса в валюте баланса', default=None)
    currency: Optional[PayoutCurrency] = Field(description='Валюта выплаты', default=None)
    account_currency: Optional[_BalanceCurrency] = Field(description='Валюта баланса', default=None)
    created_at: Optional[datetime] = Field(description='Дата и время создания выплаты', default=None)
    error_code: Optional[int] = Field(description='Код ошибки', default=None)
    error_message: Optional[str] = Field(description='Описание ошибки', default=None)


class SBPBank(BaseModel):
    member_id: Optional[int] = Field(description='Member ID банка в системе СБП', default=None)
    name: Optional[str] = Field(description='Название банка', default=None)
    name_en: Optional[str] = Field(description='Название банка на английском языке', default=None)
    bic: Optional[int] = Field(description='БИК банка', default=None)


class Refund(BaseModel):
    id: Optional[str] = Field(description='Уникальный идентификатор возврата', default=None)
    status: Optional[RefundStatus] = Field(description='Статус возврата', default=None)
    amount: Optional[Decimal] = Field(description='Сумма возврата', default=None)
    currency: Optional[RefundCurrency] = Field(description='Валюта', default=None)
    entity_type: Optional[EntityType] = Field(description='Тип возврата', default=None)
    entity_id: Optional[str] = Field(description='Уникальный идентификатор платежа, по которому производится возврат', default=None)
    created_at: Optional[datetime] = Field(description='Дата и время создания возврата', default=None)


# Модели Postback запросов

class PaymentPostbackRequest(BaseModel):
    """
    Уведомление о выполнении платежа

    В результате выполнения платежа, на Result URL, указанный в настройках магазина, отправляется POST запрос с информацией о платеже. Запрос отправляется в формате `application/x-www-form-urlencoded`. Если по какой-либо причине ваш сервер не ответил кодом 200, то уведомление будет отправлено еще раз. Стратегия переотправки postback экспоненциальная: 1 раз в 10 ^ номер попытки секунд (10 сек, 100 сек, 1000 сек...). Всего 5 попыток переотправки.
    """
    InvId: Optional[str] = Field(description='Уникальный идентификатор заказа, переданный при формировании счета', default=None)
    OutSum: Optional[Decimal] = Field(description='Сумма платежа', default=None)
    Commission: Optional[Decimal] = Field(description='Комиссия с платежа', default=None)
    TrsId: Optional[str] = Field(description='Уникальный идентификатор счета', default=None)
    Status: Optional[PaymentStatus] = Field(description='Статус платежа', default=None)
    CurrencyIn: Optional[BillCurrency] = Field(description='Валюта, в которой оплачивался счет', default=None)
    custom: Optional[str] = Field(description='Произвольное поле, переданное при формировании счета', default=None)
    AccountType: Optional[PaymentPostbackAccountType] = Field(description='Метод оплаты', default=None)
    AccountNumber: Optional[str] = Field(description='Дополнительная информация о методе оплаты', default=None)
    BalanceAmount: Optional[Decimal] = Field(description='Сумма, которая зачислена на баланс', default=None)
    BalanceCurrency: Optional[_BalanceCurrency] = Field(description='Валюта, в которой было зачисление денежных средств на баланс', default=None)
    PayerPhone: Optional[str] = Field(description='Телефон плательщика', default=None)
    PayerEmail: Optional[str] = Field(description='Почта плательщика', default=None)
    PayerName: Optional[str] = Field(description='Имя плательщика', default=None)
    PayerComment: Optional[str] = Field(description='Комментарий плательщика', default=None)
    ErrorCode: Optional[int] = Field(description='Код ошибки', default=None)
    ErrorMessage: Optional[str] = Field(description='Описание ошибки', default=None)
    SignatureValue: Optional[str] = Field(description='Подпись запроса', default=None)


class PayoutPostbackRequest(BaseModel):
    """
    Уведомление об исполнении выплаты

    В результате выполнения выплаты, если в настройках профиля указан Payout Webhook URL, отправляется POST запрос с информацией о выплате.
    """
    TrsId: Optional[str] = Field(description='Уникальный идентификатор выплаты', default=None)
    Amount: Optional[Decimal] = Field(description='Сумма выплаты вместе с комиссией', default=None)
    IsAuto: Optional[bool] = Field(description='Флаг автоматической выплаты', default=None)
    Status: Optional[PayoutPostbackStatus] = Field(description='Статус выплаты', default=None)
    Currency: Optional[PayoutPostbackCurrency] = Field(description='Валюта, в которой производится выплата', default=None)
    Commission: Optional[Decimal] = Field(description='Комиссия системы в валюте выплаты', default=None)
    AccountType: Optional[PayoutPostbackAccountType] = Field(description='Тип аккаунта, на который отправляются средства', default=None)
    AccountNumber: Optional[str] = Field(description='Идентификатор аккаунта в зависимости от AccountType: BANK_CARD - номер карты, SBP - номер телефона', default=None)
    BalanceAmount: Optional[Decimal] = Field(description='Сумма, списанная с баланса', default=None)
    BalanceCommission: Optional[Decimal] = Field(description='Комиссия системы, в валюте баланса', default=None)
    BalanceCurrency: Optional[_BalanceCurrency] = Field(description='Валюта баланса', default=None)
    CommissionApplyType: Optional[PayoutPostbackCommissionApplyType] = Field(description='Кто платил комиссию', default=None)
    SignatureValue: Optional[str] = Field(description='Подпись запроса', default=None)


class RefundPostbackRequest(BaseModel):
    """
    Уведомление об исполнении рефанда

    В результате выполнения рефанда, если в настройках магазина указан Refund URL, отправляется POST запрос с информацией о рефанде.
    """
    Id: Optional[str] = Field(description='Уникальный идентификатор рефанда', default=None)
    Amount: Optional[Decimal] = Field(description='Сумма рефанда', default=None)
    Currency: Optional[RefundPostbackCurrency] = Field(description='Валюта, в которой производится рефанд', default=None)
    Status: Optional[RefundPostbackStatus] = Field(description='Статус рефанда', default=None)
    InvId: Optional[str] = Field(description='Уникальный идентификатор заказа, переданный при формировании счета, рефанд которого выполняется', default=None)
    BillId: Optional[str] = Field(description='Уникальный идентификатор счета на оплату', default=None)
    PaymentId: Optional[str] = Field(description='Уникальный идентификатор платежа на который произошел рефанд', default=None)
    SignatureValue: Optional[str] = Field(description='Подпись запроса', default=None)


class ChargebackPostbackRequest(BaseModel):
    """
    Уведомление об исполнении чарджбэка

    В результате выполнения чарджбэка, если в настройках магазина указан Chargeback URL, отправляется POST запрос с информацией о чарджбэке.
    """
    Id: Optional[str] = Field(description='Уникальный идентификатор чарджбэка', default=None)
    Status: Optional[ChargebacPostbackStatus] = Field(description='Статус чарджбэка', default=None)
    InvId: Optional[str] = Field(description='Уникальный идентификатор заказа, переданный при формировании счета, чарджбэка которого выполняется', default=None)
    BillId: Optional[str] = Field(description='Уникальный идентификатор счета на оплату', default=None)
    PaymentId: Optional[str] = Field(description='Уникальный идентификатор платежа на который произошел чарджбэк', default=None)
    SignatureValue: Optional[str] = Field(description='Подпись запроса', default=None)


class P2PDealPayment(PaymentPostbackRequest):
    @model_validator(mode='before')
    @classmethod
    def remove_unnecessary_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Удаляем поля, которые есть в родительской модели, но отсутствуют в таблице
            fields_to_remove = [
                'custom',           # нет в таблице
                'BalanceAmount',    # нет в таблице
                'BalanceCurrency',  # нет в таблице
                'PayerPhone',       # нет в таблице
                'PayerEmail',       # нет в таблице
                'PayerName',        # нет в таблице
                'PayerComment',     # нет в таблице
            ]
            for field in fields_to_remove:
                data.pop(field, None)
        return data
    
    # Переопределяем поля, которые требуют другого поведения или описания
    InvId: Optional[str] = Field(description='Уникальный идентификатор заказа', default=None)
    OutSum: Optional[Decimal] = Field(description='Сумма платежа', default=None)
    Commission: Optional[Decimal] = Field(description='Комиссия с платежа', default=None)
    TrsId: Optional[str] = Field(description='Уникальный идентификатор счета', default=None)
    Status: Optional[PaymentStatus] = Field(description='Статус платежа', default=None)
    CurrencyIn: Optional[BillCurrency] = Field(description='Валюта, в которой оплачивался счет', default=None)
    
    # Добавляем поле AccountBank, которого нет в родительской модели
    AccountBank: Optional[str] = Field(default=None, description='Банк используемого метода оплаты')
    CommissionApplyType: Optional[P2PDealPaymentCommissionApplyType] = Field(description='Кто платил комиссию', default=None)


class P2PDealPayout(PayoutPostbackRequest):
    @model_validator(mode='before')
    @classmethod
    def remove_is_auto(cls, data: Any) -> Any:
        if isinstance(data, dict):
            data.pop('IsAuto', None)
        return data
    
    class Config:
        fields = {'IsAuto': {'exclude': True}}


class P2PDealPostbackRequest(BaseModel):
    """
    Уведомление о выполнении P2P сделки

    В результате выполнения P2P сделки, на Result URL, указанный в настройках магазина, отправляется POST запрос с информацией о платеже. Запрос отправляется в формате 'application/x-www-form-urlencoded'. Если по какой-либо причине ваш сервер не ответил кодом 200, то уведомление будет отправлено еще раз. Стратегия переотправки postback экспоненциальная: 1 раз в 10 ^ номер попытки секунд (10 сек, 100 сек, 1000 сек...). Всего 5 попыток переотправки.
    """
    TrsId: Optional[str] = Field(description='Уникальный идентификатор P2P-сделки', default=None)
    InvId: Optional[str] = Field(description='Поле order_id, передаваемое при создании P2P-сделки', default=None)
    Status: Optional[P2PDealPostbackStatus] = Field(description='Статус P2P-сделки', default=None)
    Amount: Optional[Decimal] = Field(description='Сумма сделки', default=None)
    Currency: Optional[P2PDealCurrency] = Field(description='Валюта сделки', default=None)
    BalanceAmount: Optional[Decimal] = Field(description='Сумма, зачисленная на баланс', default=None)
    BalanceCurrency: Optional[_BalanceCurrency] = Field(description='Валюта, в которой были зачислены средства на баланс', default=None)
    Payment: Optional[list[P2PDealPayment]] = Field(description='Информация о платеже', default=None)
    Payout: Optional[list[P2PDealPayout]] = None
    SignatureValue: Optional[str] = Field(description='Подпись запроса', default=None)


# Модели пагинации

class PaginationLinks(BaseModel):
    prev: Optional[str] = Field(description='Ссылка на предыдущую страницу', default=None)
    next: Optional[str] = Field(description='Ссылка на следующую страницу', default=None)


class PaginationMeta(BaseModel):
    path: Optional[str] = Field(description='Ссылка на страницу без курсора', default=None)
    per_page: Optional[int] = Field(description='Количество элементов на странице', default=None)
    prev_cursor: Optional[str] = Field(description='Указатель на предыдущую страницу', default=None)
    next_cursor: Optional[str] = Field(description='Указатель на следующую страницу', default=None)


class RequestField(BaseModel):
    email: Optional[bool] = Field(description='Обязательный запрос электронной почты у плательщика', default=None)
    phone: Optional[bool] = Field(description='Обязательный запрос номера телефона у плательщика', default=None)
    name: Optional[bool] = Field(description='Обязательный запрос ФИО у плательщика', default=None)
    comment: Optional[bool] = Field(description='Обязательный запрос комментария у плательщика', default=None)

class Item(BaseModel):
    name: Optional[str] = None
    price: Optional[Decimal] = None
    quantity: Optional[int] = None
    category: Optional[str] = None
    extra: Optional[dict] = None