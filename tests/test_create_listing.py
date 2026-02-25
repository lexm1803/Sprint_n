import allure
import pytest

from endpoints.auth_endpoint import AuthEndpoint
from endpoints.listing_endpoint import ListingEndpoint
from config.data import CATEGORIES


@allure.feature("Создание объявлений")
class TestCreateListing:

    @allure.title("Создание объявления с различными категориями")
    @allure.story("Успешное создание объявления")
    @pytest.mark.parametrize("category", CATEGORIES)
    def test_create_new_order_with_all_categories_successful_status_code_201(
        self,
        api_client,
        registered_and_auth_user,
        category,
    ):
        email, password, token = registered_and_auth_user
        
        auth = AuthEndpoint(api_client)
        auth.get_token(email, password)

        listings = ListingEndpoint(api_client)
        response = listings.create_with_category(category)

        assert response.status_code == 201
        assert response.body.category == category
