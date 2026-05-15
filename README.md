# Cardlink API Client

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/pycardlink.svg)](https://pypi.org/project/pycardlink/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Асинхронный и синхронный Python-клиент для [CardLink API](https://cardlink.link/reference/api).**

Библиотека предоставляет удобный, типобезопасный интерфейс для взаимодействия с платежной системой CardLink. Она поддерживает все основные операции: создание счетов, выплаты, возвраты, управление балансом и поиск транзакций. Клиент полностью типизирован с использованием `pydantic` и `httpx`.

---

## Возможности

- 🚀 **Асинхронный и синхронный клиент** — выбирайте подходящий стиль взаимодействия.
- 📦 **Строгая типизация** — все модели запросов и ответов описаны с помощью Pydantic.
- 🔑 **Простая аутентификация** — достаточно передать API-ключ при создании клиента.
- 🌐 **Полный охват API** — поддерживаются счета, платежи, выплаты, возвраты, баланс и поиск.
- 🛡️ **Встроенная обработка ошибок** — понятные исключения при сетевых сбоях или ошибках API.
- ⚙️ **Гибкая конфигурация** — можно задать собственный `base_url` для работы с тестовым окружением.

---

## Установка

Убедитесь, что у вас установлен Python 3.10 или выше. Затем выполните:

```bash
pip install pycardlink
```

Либо, если вы используете `uv`:

```bash
uv add pycardlink
```

---

## Быстрый старт

### 1. Получите API-ключ и Shop ID

1. Зарегистрируйтесь на [cardlink.link](https://cardlink.link/).
2. Создайте магазин и дождитесь его одобрения.
3. В личном кабинете вы найдете **API-ключ** и **Shop ID**.

### 2. Создание счета (асинхронный клиент)

```python
import asyncio
from pycardlink import CardLinkAsyncClient
from pycardlink.models.requests import BillCreateRequest

async def main():
    client = CardLinkAsyncClient(api_key="your_api_key")
    
    # Создаём счёт на 100 рублей
    bill = await client.bill.create(
        BillCreateRequest(
            amount=100.0,
            shop_id="shop_123",
            description="Оплата заказа №42",
            order_id="order_42"
        )
    )
    
    print(f"Счёт создан: {bill.link_url}")

asyncio.run(main())
```

### 3. Создание счета (синхронный клиент)

```python
from pycardlink import CardLinkSyncClient
from pycardlink.models.requests import BillCreateRequest

client = CardLinkSyncClient(api_key="your_api_key")

bill = client.bill.create(
    BillCreateRequest(
        amount=100.0,
        shop_id="shop_123",
        description="Оплата заказа №42",
        order_id="order_42"
    )
)

print(f"Счёт создан: {bill.link_url}")
```

---

## Документация

### Структура проекта

```
pycardlink/
├── __init__.py          # Точка входа, версия, экспорт
├── clients.py           # Асинхронный (CardLinkAsyncClient) и синхронный (CardLinkSyncClient) клиенты
├── controllers.py       # Контроллеры для каждого раздела API (Bill, Payment, Payout, Refund, Balance)
└── models/
    ├── __init__.py
    ├── data.py          # Pydantic-модели данных (Bill, Payment, Payout и др.)
    ├── enums.py         # Перечисления (BillStatus, PaymentCurrency и т.д.)
    └── requests.py      # Модели запросов и ответов (BillCreateRequest, PaymentSearchRequest и т.д.)
```

### Доступные контроллеры

Каждый клиент (`CardLinkAsyncClient` / `CardLinkSyncClient`) предоставляет следующие контроллеры:

| Контроллер | Методы |
|------------|--------|
| `client.bill` | `create()`, `toggle_activity()`, `payments()`, `search()`, `status()` |
| `client.payment` | `search()`, `status()` |
| `client.payout` | `create_personal()`, `create_regular()`, `search()`, `status()`, `spb_banks()` |
| `client.refund` | `create_full()`, `create_partial()`, `search()`, `status()` |
| `client.balance` | `get_merchant_balance()` |

### Модели запросов и ответов

Все модели находятся в пакете `pycardlink.models.requests` и `pycardlink.models.data`. Благодаря Pydantic вы получаете автоматическую валидацию данных, подсказки в IDE и сериализацию/десериализацию.

Пример:

```python
from pycardlink.models.requests import PaymentSearchRequest
from pycardlink.models.enums import PaymentStatus

search = PaymentSearchRequest(
    bill_id="bill_123",
    status=PaymentStatus.SUCCESS,
    limit=20
)
```

### Обработка ошибок

Библиотека выбрасывает понятные исключения:

- `RuntimeError` — ошибка, возвращённая API (например, неверный запрос).
- `ConnectionError` — проблемы с сетью или недоступность сервера.

```python
try:
    bill = await client.bill.create(...)
except RuntimeError as e:
    print(f"Ошибка API: {e}")
except ConnectionError as e:
    print(f"Сетевая ошибка: {e}")
```

---

## Разработка

### Сборка и тестирование

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/austnv/pycardlink.git
   cd pycardlink
   ```

2. Установите зависимости:
   ```bash
   uv sync
   ```

3. Запустите линтеры (если настроены):
   ```bash
   ruff check .
   ```

### Участие в разработке

Мы приветствуем ваши предложения и pull request'ы! Пожалуйста, открывайте issue для обсуждения предлагаемых изменений перед отправкой PR.

---

## Лицензия

Проект распространяется под лицензией MIT. Подробности см. в файле [LICENSE](LICENSE).

---

## Ссылки

- [Документация CardLink API](https://cardlink.link/reference/api)
- [Официальный сайт CardLink](https://cardlink.link/)
- [Репозиторий на GitHub](https://github.com/austnv/pycardlink)
