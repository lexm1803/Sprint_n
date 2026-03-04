import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from wrappers.response_wrapper import ResponseWrapper
from config.data import (
    AuthResponse,
    RegisterResponse,
    ListingResponse,
    UpdateResponse,
    DeleteResponse,
    ErrorResponse,
)


class BaseClient:

    def __init__(self, base_url, auth_token=None):
        self.base_url = base_url
        self.auth_token = auth_token
        self.session = requests.Session()
        if auth_token:
            self.session.headers.update({"Authorization": auth_token})

    def wrap_response(self, response, success_model, error_model=ErrorResponse):
        status_code = response.status_code
        headers = dict(response.headers)

        try:
            json_data = response.json()
        except ValueError:
            json_data = {"message": response.text}

        if 200 <= status_code < 300:
            body = success_model.model_validate(json_data)
        else:
            body = error_model.model_validate(json_data)

        return ResponseWrapper(
            status_code=status_code,
            body=body,
            headers=headers,
            raw_response=response,
        )

    def post(self, endpoint, data=None, json=None, headers=None):
        request_headers = self.get_headers(headers)
        return self.session.post(
            f"{self.base_url}{endpoint}",
            data=data,
            json=json,
            headers=request_headers,
            verify=False,
        )

    def post_multipart(self, endpoint, files, headers=None):
        request_headers = self.get_headers(headers)
        multipart_data = MultipartEncoder(fields=files)
        request_headers["Content-Type"] = multipart_data.content_type
        return self.session.post(
            f"{self.base_url}{endpoint}",
            data=multipart_data,
            headers=request_headers,
            verify=False,
        )

    def patch(self, endpoint, files=None, headers=None):
        request_headers = self.get_headers(headers)
        multipart_data = MultipartEncoder(fields=files)
        request_headers["Content-Type"] = multipart_data.content_type
        return self.session.patch(
            f"{self.base_url}{endpoint}",
            data=multipart_data,
            headers=request_headers,
            verify=False,
        )

    def delete(self, endpoint, headers=None):
        request_headers = self.get_headers(headers)
        return self.session.delete(
            f"{self.base_url}{endpoint}",
            headers=request_headers,
            verify=False,
        )

    def get_headers(self, extra_headers=None):
        headers = {}
        if self.auth_token:
            headers["Authorization"] = self.auth_token
        if extra_headers:
            headers.update(extra_headers)
        return headers

    def set_auth_token(self, token):
        self.auth_token = token
        self.session.headers.update({"Authorization": token})

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
