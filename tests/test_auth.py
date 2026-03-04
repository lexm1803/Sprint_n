import allure

from endpoints.auth_endpoint import AuthEndpoint
from config.data import AuthData


@allure.feature("Авторизация")
class TestAuth:

    @allure.title("Успешная авторизация зарегистрированного пользователя")
    @allure.story("Авторизация с валидными данными")
    def test_auth_user_with_valid_data_status_code_201(
        self,
        api_client,
        registered_and_auth_user,
    ):
        email, password, _, _ = registered_and_auth_user
        auth = AuthEndpoint(api_client)
        data = AuthData(email=email, password=password)
        response = auth.auth(data)

        assert response.status_code == 201
        assert response.body.user.email == email
