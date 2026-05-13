"""
Enums
"""

from enum import Enum


class BillStatus(Enum):
    NEW = "NEW"
    PROCESS = "PROCESS"
    UNDERPAID = "UNDERPAID"
    SUCCESS = "SUCCESS"
    OVERPAID = "OVERPAID"
    FAIL = "FAIL"


class BillType(Enum):
    MULTI = "MULTI"
    NORMAL = "NORMAL"


class BillCurrency(Enum):
    USD = "USD"
    RUB = "RUB"
    EUR = "EUR"


class PaymentStatus(Enum):
    NEW = "NEW"
    PROCESS = "PROCESS"
    UNDERPAID = "UNDERPAID"
    SUCCESS = "SUCCESS"
    OVERPAID = "OVERPAID"
    FAIL = "FAIL"


class PaymentCurrency(Enum):
    USD = "USD"
    RUB = "RUB"
    EUR = "EUR"


class ChargebackStatus(Enum):
    NEW = "NEW"
    PROCESS = "PROCESS"
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"


class _BalanceCurrency(Enum):
    USD = "USD"
    RUB = "RUB"
    EUR = "EUR"


class PayoutStatus(Enum):
    NEW = "NEW"
    MODERATING = "MODERATING"
    PROCESS = "PROCESS"
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"
    ERROR = "ERROR"
    DECLINED = "DECLINED"


class PayoutCurrency(Enum):
    USD = "USD"
    RUB = "RUB"
    EUR = "EUR"


class RefundStatus(Enum):
    NEW = "NEW"
    PROCESS = "PROCESS"
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"


class RefundCurrency(Enum):
    USD = "USD"
    RUB = "RUB"
    EUR = "EUR"


class EntityType(Enum):
    PAYMENT = "payment"


class PaymentPostbackAccountType(Enum):
    BANK_CARD = "BANK_CARD"
    SBP = "SBP"


class PaymentPostbackStatus(Enum):
    SUCCESS = "SUCCESS"
    UNDERPAID = "UNDERPAID"
    OVERPAID = "OVERPAID"
    FAIL = "FAIL"


class PayoutPostbackStatus(Enum):
    SUCCESS = "SUCCESS"
    DECLINED = "DECLINED"
    FAIL = "FAIL"


class PayoutPostbackCurrency(Enum):
    USD = "USD"
    RUB = "RUB"
    EUR = "EUR"
    USDT = "USDT"


class PayoutPostbackAccountType(Enum):
    BANK_CARD = "BANK_CARD"
    SBP = "SBP"
    CRYPTO = "CRYPTO"


class PayoutPostbackCommissionApplyType(Enum):
    SENDER = "sender"
    RECIPIENT = "recipient"


class RefundPostbackCurrency(Enum):
    USD = "USD"
    RUB = "RUB"
    EUR = "EUR"
    USDT = "USDT"


class RefundPostbackStatus(Enum):
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"


class ChargebacPostbackStatus(Enum):
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"


class P2PDealPostbackStatus(Enum):
    NEW = "NEW"
    PROCESS = "PROCESS"
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"


class P2PDealCurrency(Enum):
    USD = "USD"
    RUB = "RUB"
    EUR = "EUR"


class P2PDealPaymentCommissionApplyType(Enum):
    PAYER = "payer"
    RECIPIENT = "recipient"


class Locale(Enum):
    RU = "ru"
    EN = "en"


class PaymentMethod(Enum):
    BANK_CARD = "BANK_CARD"
    SBP = "SBP"


class PayoutAccountType(Enum):
    CREDIT_CARD = "credit_card"
    SBP = "sbp"
    CRYPTO = "crypto"
    STEAM = "steam"


class PayoutAccountNetwork(Enum):
    TRX = "TRX"
    ETH = "ETH"