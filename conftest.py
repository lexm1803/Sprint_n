import pytest
import allure

from clients.api_client import APIClient
from endpoints.auth_endpoint import AuthEndpoint
from endpoints.register_endpoint import RegisterEndpoint
from endpoints.listing_endpoint import ListingEndpoint
from config.data import CATEGORIES
from utils.generators import UserDataGenerator


@pytest.fixture
def api_client():
    client = APIClient()
    yield client
    client.close()


@pytest.fixture
def registered_and_auth_user(api_client):
    email, password = UserDataGenerator.generate()
    register = RegisterEndpoint(api_client)
    register.register_with_email(email, password)
    
    auth = AuthEndpoint(api_client)
    token = auth.get_token(email, password)
    created_order_ids = []
    yield email, password, token, created_order_ids

    api_client.set_auth_token(f'Bearer {token}')
    listings = ListingEndpoint(api_client)
    for order_id in created_order_ids:
        try:
            listings.delete(order_id)
        except Exception:
            pass
    
    try:
        api_client.delete('/api/v1/user')
    except Exception:
        pass

@pytest.fixture
def get_auth_token(registered_and_auth_user):
    return registered_and_auth_user[2]


@pytest.fixture
def get_auth_token_and_order_id(api_client, registered_and_auth_user):
    email, password, token, created_order_ids = registered_and_auth_user
    listings = ListingEndpoint(api_client)
    response = listings.create_with_category("Авто")
    order_id = response.body.id
    created_order_ids.append(order_id) # type: ignore
    return token, order_id


@pytest.fixture
def second_registered_and_auth_user(api_client):
    email, password = UserDataGenerator.generate()
    register = RegisterEndpoint(api_client)
    register.register_with_email(email, password)
    
    auth = AuthEndpoint(api_client)
    token = auth.get_token(email, password)
    created_order_ids = []
    yield email, password, token, created_order_ids

    api_client.set_auth_token(f'Bearer {token}')
    listings = ListingEndpoint(api_client)
    for order_id in created_order_ids:
        try:
            listings.delete(order_id)
        except Exception:
            pass
    try:
        api_client.delete('/api/v1/user')
    except Exception:
        pass


@pytest.fixture
def second_user_token(second_registered_and_auth_user):
    return second_registered_and_auth_user[2]


@pytest.fixture(params=CATEGORIES, ids=lambda x: x)
def category(request):
    return request.param

@pytest.fixture
def clean_up_user_data(api_client):
    def clean_up(token):
        api_client.set_auth_token(token)
        try:
            api_client.delete('/api/v1/user')
        except Exception:
            pass
        
    yield clean_up
    