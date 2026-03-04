import allure

from clients.base_client import BaseClient
from config.data import (
    UPDATE_ORDER_URL,
    UpdateListingData,
    UpdateResponse,
    ErrorResponse,
)


class UpdateEndpoint:

    def __init__(self, client):
        self.client = client

    @allure.step("Обновление объявления")
    def update(self, order_id, data):
        files = {k: (None, str(v)) for k, v in data.model_dump().items()}
        endpoint = f"{UPDATE_ORDER_URL}{order_id}"
        response = self.client.patch(endpoint, files=files)
        return self.client.wrap_response(response, UpdateResponse, ErrorResponse)

    @allure.step("Обновление названия объявления")
    def update_name(self, order_id, new_name):
        data = UpdateListingData(name=new_name)
        return self.update(order_id, data)
