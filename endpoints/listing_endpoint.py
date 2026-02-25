import allure

from clients.base_client import BaseClient
from config.data import (
    CREATE_LISTING_URL,
    DELETE_ORDER_URL,
    CreateListingData,
    ListingResponse,
    DeleteResponse,
    ErrorResponse,
)


class ListingEndpoint:

    def __init__(self, client):
        self.client = client

    @allure.step("Создание нового объявления")
    def create(self, data):
        files = {k: (None, str(v)) for k, v in data.model_dump().items()}
        response = self.client.post_multipart(CREATE_LISTING_URL, files=files)
        return self.client.wrap_response(response, ListingResponse, ErrorResponse)

    @allure.step("Создание объявления с категорией")
    def create_with_category(self, category):
        data = CreateListingData(category=category)
        return self.create(data)

    @allure.step("Удаление объявления")
    def delete(self, order_id):
        endpoint = f"{DELETE_ORDER_URL}{order_id}"
        response = self.client.delete(endpoint)
        return self.client.wrap_response(response, DeleteResponse, ErrorResponse)
