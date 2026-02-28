# API Test Framework

Фреймворк для автоматизированного тестирования API доски объявлений.

## Архитектура

Паттерны проектирования:
- **Facade** — `APIClient` для высокоуровневого доступа к API
- **Builder** — `ListingDataBuilder` для гибкого создания данных
- **ResponseWrapper** — универсальная обёртка ответов с типизацией

## Структура проекта

```
sprint_m_api/
├── config/              # Константы и Pydantic модели
│   └── data.py
├── clients/             # HTTP клиенты (requests)
│   ├── base_client.py   # Базовый клиент
│   └── api_client.py    # Facade
├── endpoints/           # API endpoints
│   ├── auth_endpoint.py
│   ├── register_endpoint.py
│   ├── listing_endpoint.py
│   └── update_endpoint.py
├── utils/               # Утилиты и хелперы
│   ├── generators.py    # Генераторы данных
│   └── builders.py      # Builders
├── wrappers/            # Response обёртки
│   └── response_wrapper.py
├── tests/               # Тесты
│   ├── test_auth.py
│   ├── test_register.py
│   ├── test_create_listing.py
│   ├── test_listings.py
│   └── test_update_offer.py
├── conftest.py          # Pytest фикстуры
├── pytest.ini           # Pytest конфигурация
├── requirements.txt     # Зависимости
└── README.md
```

## Быстрый старт

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Запуск тестов

```bash
# Все тесты
pytest

# С отчётом Allure
pytest --alluredir=allure_results

# Открыть отчёт
allure serve allure_results
```

### Отдельные тесты

```bash
# Конкретный файл
pytest tests/test_register.py -v

# Конкретный тест
pytest tests/test_register.py::TestRegister::test_register_new_user_with_unique_email_status_code_201 -v
```

## Примеры использования

### APIClient (Facade)

```python
from clients.api_client import APIClient

client = APIClient()
client.auth_with_token("email@example.com", "password")

from config.data import CreateListingData
data = CreateListingData(category="Авто")
response = client.create_listing(data)
print(response.body.id)

client.delete_listing(order_id)
```

### Endpoints

```python
from clients.api_client import APIClient
from endpoints.auth_endpoint import AuthEndpoint
from endpoints.listing_endpoint import ListingEndpoint

client = APIClient()
auth = AuthEndpoint(client)
listings = ListingEndpoint(client)

token = auth.get_token("email@example.com", "password")
response = listings.create_with_category("Книги")
```

### Builders

```python
from utils.builders import ListingDataBuilder

data = (ListingDataBuilder()
    .with_name("Товар")
    .with_category("Авто")
    .with_price(500000)
    .build_create())

# Быстрый способ
data = ListingDataBuilder.with_category_only("Технологии")
```

### Generators

```python
from utils.generators import EmailGenerator, ListingDataGenerator

# Email
email = EmailGenerator.generate()

# Данные объявления
data = ListingDataGenerator.create("Авто")
random_data = ListingDataGenerator.create_random()
```

## Pydantic модели

**Request:** `AuthData`, `RegisterData`, `CreateListingData`, `UpdateListingData`

**Response:** `AuthResponse`, `RegisterResponse`, `ListingResponse`, `UpdateResponse`, `DeleteResponse`, `ErrorResponse`

## Особенности

- requests — HTTP клиент
- requests-toolbelt — multipart/form-data
- Типизация через Pydantic
- Allure отчёты
- Чистая архитектура
- http метод delete не реализован на бэкенде