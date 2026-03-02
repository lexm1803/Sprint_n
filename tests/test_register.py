import allure

from endpoints.register_endpoint import RegisterEndpoint
from config.data import ERROR_REGISTER_NOT_UNIQUE_EMAIL
from utils.generators import UserDataGenerator


@allure.feature("Регистрация")
class TestRegister:

    @allure.title("Регистрация пользователя с уникальным email")
    @allure.story("Успешная регистрация")
    def test_register_new_user_with_unique_email_status_code_201(
        self,
        api_client,
    ):
        email, password = UserDataGenerator.generate()
        register = RegisterEndpoint(api_client)
        response = register.register_with_email(email, password)

        assert response.status_code == 201
        assert response.body.user.email == email

    @allure.title("Регистрация пользователя с не уникальным email")
    @allure.story("Ошибка регистрации - email уже используется")
    def test_register_new_user_with_not_unique_email_status_code_400(
        self,
        api_client,
    ):
        email, password = UserDataGenerator.generate()
        register = RegisterEndpoint(api_client)

        register.register_with_email(email, password)
        response = register.register_with_email(email, password)

        assert response.status_code == 400
        assert response.body.message == ERROR_REGISTER_NOT_UNIQUE_EMAIL
