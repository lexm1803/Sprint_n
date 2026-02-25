import allure

from endpoints.listing_endpoint import ListingEndpoint
from config.data import SUCCESSFUL_ORDER_DELETE_TEXT


@allure.feature("Удаление объявлений")
class TestDeleteListing:

    @allure.title("Удаление объявления создателем")
    @allure.story("Успешное удаление объявления")
    def test_delete_order_created_by_auth_user_status_code_200(
        self,
        api_client,
        get_auth_token_and_order_id,
    ):
        token, order_id = get_auth_token_and_order_id

        listings = ListingEndpoint(api_client)
        response = listings.delete(order_id)

        assert response.status_code == 200
        assert response.body.message == SUCCESSFUL_ORDER_DELETE_TEXT
