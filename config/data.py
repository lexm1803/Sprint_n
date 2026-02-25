from enum import Enum
from pydantic import BaseModel, Field


BASE_URL = "https://qa-desk.stand.praktikum-services.ru/api/"
REGISTER_URL = "signup"
AUTH_URL = "signin"
CREATE_LISTING_URL = "create-listing"
UPDATE_ORDER_URL = "update-offer/"
DELETE_ORDER_URL = "listings/"

ERROR_REGISTER_NOT_UNIQUE_EMAIL = "Почта уже используется"
ERROR_EDIT_ORDER_WITHOUT_AUTH = "Оффер не найден или у вас нет прав на его редактирование"
SUCCESSFUL_ORDER_DELETE_TEXT = "Объявление удалено успешно"


class ListingCategory(str, Enum):
    AUTO = "Авто"
    BOOKS = "Книги"
    GARDENING = "Садоводство"
    HOBBIES = "Хобби"
    TECHNOLOGIES = "Технологии"


class ListingCondition(str, Enum):
    NEW = "Новый"
    USED = "Б/у"


CATEGORIES = [category.value for category in ListingCategory]


class RegisterData(BaseModel):
    email: str
    password: str
    submitPassword: str

    @classmethod
    def from_email(cls, email, password=None):
        pwd = password if password else email
        return cls(email=email, password=pwd, submitPassword=pwd)


class AuthData(BaseModel):
    email: str
    password: str


class CreateListingData(BaseModel):
    name: str = ""
    category: str
    condition: str = ListingCondition.NEW.value
    city: str = "Москва"
    description: str = ""
    price: int = 0


class UpdateListingData(BaseModel):
    name: str
    category: str = ListingCategory.AUTO.value
    condition: str = ListingCondition.NEW.value
    city: str = "Москва"
    description: str = ""
    price: int = 0
    img1: None = None
    img2: None = None
    img3: None = None


class TokenData(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserData(BaseModel):
    email: str
    id: int | str


class AuthResponse(BaseModel):
    token: TokenData
    user: UserData


class RegisterResponse(BaseModel):
    user: UserData


class ListingResponse(BaseModel):
    id: int | str
    name: str
    category: str
    condition: str
    city: str
    description: str
    price: int
    ownerId: int | str | None = None
    createdAt: str | None = None
    updatedAt: str | None = None
    isFavorite: bool | None = None


class UpdateResponse(BaseModel):
    id: int | str
    name: str
    category: str
    condition: str
    city: str
    description: str
    price: int
    ownerId: int | str | None = None
    createdAt: str | None = None
    updatedAt: str | None = None
    isFavorite: bool | None = None


class DeleteResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    message: str
    error: str | None = None
