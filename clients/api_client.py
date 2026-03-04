import allure

from clients.base_client import BaseClient
from config.data import (
    BASE_URL,
    REGISTER_URL,
    AUTH_URL,
    CREATE_LISTING_URL,
    UPDATE_ORDER_URL,
    DELETE_ORDER_URL,
    AuthData,
    RegisterData,
    CreateListingData,
    UpdateListingData,
    AuthResponse,
    RegisterResponse,
    ListingResponse,
    UpdateResponse,
    DeleteResponse,
    ErrorResponse,
)


class APIClient(BaseClient):

    def __init__(self, auth_token=None):
        super().__init__(BASE_URL, auth_token)

    @allure.step("Регистрация пользователя")
    def register(self, data):
        response = self.post(REGISTER_URL, data=data.model_dump())
        return self.wrap_response(response, RegisterResponse, ErrorResponse)

    @allure.step("Регистрация с email")
    def register_with_email(self, email):
        data = RegisterData.from_email(email)
        return self.register(data)

    @allure.step("Авторизация пользователя")
    def auth(self, data):
        response = self.post(AUTH_URL, data=data.model_dump())
        return self.wrap_response(response, AuthResponse, ErrorResponse)

    @allure.step("Получение токена авторизации")
    def auth_with_token(self, email, password):
        data = AuthData(email=email, password=password)
        response = self.auth(data)
        token = f"Bearer {response.body.token.access_token}"
        self.set_auth_token(token)
        return token

    @allure.step("Создание объявления")
    def create_listing(self, data):
        files = {k: (None, str(v)) for k, v in data.model_dump().items()}
        response = self.post_multipart(CREATE_LISTING_URL, files=files)
        return self.wrap_response(response, ListingResponse, ErrorResponse)

    @allure.step("Создание объявления с категорией")
    def create_listing_with_category(self, category):
        data = CreateListingData(category=category)
        return self.create_listing(data)

    @allure.step("Обновление объявления")
    def update_listing(self, order_id, data):
        files = {k: (None, str(v)) for k, v in data.model_dump().items()}
        endpoint = f"{UPDATE_ORDER_URL}{order_id}"
        response = self.patch(endpoint, files=files)
        return self.wrap_response(response, UpdateResponse, ErrorResponse)

    @allure.step("Обновление названия объявления")
    def update_listing_name(self, order_id, new_name):
        data = UpdateListingData(name=new_name)
        return self.update_listing(order_id, data)

    @allure.step("Удаление объявления")
    def delete_listing(self, order_id):
        endpoint = f"{DELETE_ORDER_URL}{order_id}"
        response = self.delete(endpoint)
        return self.wrap_response(response, DeleteResponse, ErrorResponse)
