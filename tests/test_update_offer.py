import allure

from endpoints.update_endpoint import UpdateEndpoint
from config.data import ERROR_EDIT_ORDER_WITHOUT_AUTH


@allure.feature("Обновление объявлений")
class TestUpdateOrder:

    @allure.title("Редактирование объявления создателем")
    @allure.story("Успешное обновление объявления")
    def test_update_order_created_by_auth_user_status_code_200(
        self,
        api_client,
        get_auth_token_and_order_id,
    ):
        token, order_id = get_auth_token_and_order_id

        update = UpdateEndpoint(api_client)
        response = update.update_name(order_id, "Новое название")

        assert response.status_code == 200
        assert response.body.name == "Новое название"

    @allure.title("Редактирование объявления чужим пользователем")
    @allure.story("Ошибка обновления - нет прав доступа")
    def test_update_order_not_created_by_auth_user_status_code_401(
        self,
        api_client,
        get_auth_token_and_order_id,
        second_user_token,
    ):
        _, order_id = get_auth_token_and_order_id

        api_client.set_auth_token(second_user_token)

        update = UpdateEndpoint(api_client)
        response = update.update_name(order_id, "Новое название")

        assert response.status_code == 401
        assert response.body.message == ERROR_EDIT_ORDER_WITHOUT_AUTH
