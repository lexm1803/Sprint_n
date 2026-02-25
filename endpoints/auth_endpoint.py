import allure

from clients.base_client import BaseClient
from config.data import AUTH_URL, AuthData, AuthResponse, ErrorResponse


class AuthEndpoint:

    def __init__(self, client):
        self.client = client

    @allure.step("Авторизация пользователя")
    def auth(self, data):
        response = self.client.post(AUTH_URL, data=data.model_dump())
        return self.client.wrap_response(response, AuthResponse, ErrorResponse)

    @allure.step("Получение токена авторизации")
    def get_token(self, email, password):
        data = AuthData(email=email, password=password)
        response = self.auth(data)
        token = f"Bearer {response.body.token.access_token}"
        self.client.set_auth_token(token)
        return token
