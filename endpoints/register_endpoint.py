import allure

from clients.base_client import BaseClient
from config.data import REGISTER_URL, RegisterData, RegisterResponse, ErrorResponse


class RegisterEndpoint:

    def __init__(self, client):
        self.client = client

    @allure.step("Регистрация нового пользователя")
    def register(self, data):
        response = self.client.post(REGISTER_URL, data=data.model_dump())
        return self.client.wrap_response(response, RegisterResponse, ErrorResponse)

    @allure.step("Регистрация с email")
    def register_with_email(self, email, password=None):
        data = RegisterData.from_email(email, password)
        return self.register(data)
