import pytest
import allure

from clients.api_client import APIClient
from endpoints.auth_endpoint import AuthEndpoint
from endpoints.register_endpoint import RegisterEndpoint
from endpoints.listing_endpoint import ListingEndpoint
from config.data import CATEGORIES
from utils.generators import UserDataGenerator


@pytest.fixture
def registered_user():
    email, password = UserDataGenerator.generate()
    return email, password


@pytest.fixture
def api_client():
    client = APIClient()
    yield client
    client.close()


@pytest.fixture
def registered_and_auth_user(api_client, registered_user):
    email, password = registered_user
    register = RegisterEndpoint(api_client)
    register.register_with_email(email, password)
    
    auth = AuthEndpoint(api_client)
    token = auth.get_token(email, password)
    return email, password, token


@pytest.fixture
def get_auth_token(registered_and_auth_user):
    return registered_and_auth_user[2]


@pytest.fixture
def get_auth_token_and_order_id(api_client, registered_and_auth_user):
    email, password, token = registered_and_auth_user
    listings = ListingEndpoint(api_client)
    response = listings.create_with_category("Авто")
    order_id = response.body.id
    return token, order_id


@pytest.fixture
def second_registered_and_auth_user(api_client):
    email, password = UserDataGenerator.generate()
    register = RegisterEndpoint(api_client)
    register.register_with_email(email, password)
    
    auth = AuthEndpoint(api_client)
    token = auth.get_token(email, password)
    return email, password, token


@pytest.fixture
def second_user_token(second_registered_and_auth_user):
    return second_registered_and_auth_user[2]


@pytest.fixture(params=CATEGORIES, ids=lambda x: x)
def category(request):
    return request.param
