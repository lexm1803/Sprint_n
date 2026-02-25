from pydantic import BaseModel, Field


class ResponseWrapper(BaseModel):
    status_code: int
    body: BaseModel
    headers: dict = Field(default_factory=dict)
    raw_response: object = Field(default=None, exclude=True)

    @property
    def is_success(self):
        return 200 <= self.status_code < 300

    @property
    def is_created(self):
        return self.status_code == 201

    @property
    def is_ok(self):
        return self.status_code == 200

    @property
    def is_client_error(self):
        return 400 <= self.status_code < 500

    @property
    def is_server_error(self):
        return 500 <= self.status_code < 600

    def get_header(self, name, default=None):
        return self.headers.get(name, default)

    def __str__(self):
        return f"ResponseWrapper(status_code={self.status_code}, body={self.body})"
