import requests
from pandas import Series, to_datetime
from getpass import getpass
# typing
from pydantic import (BaseModel, SecretStr,
                      field_validator, EmailStr, ConfigDict)
from typing import Optional
from dataclasses import field
# api endpoints
from .constants import API_ENDPOINTS


class WatersyncResponse(BaseModel):
    """
    Stores and validates the response from the API.

    Attributes:
        response (requests.Response): The response from the API.

    Properties:
        status_code (int): The status code of the response.
        headers (dict): The headers of the response.
        fail (str): A message that describes the failure of the response.
        content (dict): The content of the response.
        timeseries (pandas.Series): The timeseries data from the response.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    response: requests.Response

    @property
    def status_code(self) -> int:
        return self.response.status_code

    @property
    def headers(self) -> dict:
        return dict(self.response.headers)

    @property
    def fail(self) -> str:
        return f'Status {self.status_code}: {self.response.content.decode()}'

    @property
    def content(self) -> dict | str:
        if self.status_code == 200:
            return self.response.json()
        elif self.status_code in [204, 404]:
            return "No content found."
        else:
            return self.fail

    @property
    def timeseries(self) -> Series:

        values = self.content.get('value')
        timestamps = self.content.get('timestamp')

        if not isinstance(values, list) or not isinstance(timestamps, list):
            raise Exception("Timeseries data not found.")

        return Series(data=values, index=to_datetime(timestamps, utc=True))


class WatersyncRequest(BaseModel):
    """
    Stores and validates the information needed to make a request to the API.

    Some of the basic information (base_url, endpoint, project) can be unpacked from 
    a WaterDataClient object.

    Attributes:
        base_url (str): The base url of the API.
        endpoint (str): The endpoint of the API.
        project (str): The project name.
        token (SecretStr): The token needed to authenticate with the API.
        data (dict | list): The data to be sent with the request.
        headers (dict): The headers to be sent with the request.
        params (dict): The parameters to be sent with the request.

    Properties:
        full_url (str): The full url of the request.

    Methods:
        post: Make a POST request to the API.
        get: Make a GET request to the API.
        delete: Make a DELETE request to the API.
        patch: Make a PATCH request to the API.
    """
    base_url: str
    endpoint: str
    project: Optional[str] = None
    token: Optional[SecretStr] = field(default=None, repr=False)
    data: Optional[dict | list] = {}
    headers: dict = {}
    params: dict = {}

    @field_validator('base_url')
    def ensure_trailing_slash_in_base_url(cls, v):
        if not v.endswith('/'):
            return f"{v}/"
        return v

    @field_validator('endpoint')
    def ensure_no_leading_slash_in_endpoint(cls, v):
        if v.startswith('/'):
            return v[1:]
        return v

    @field_validator('endpoint')
    def ensure_trailing_slash_in_endpoint(cls, v):
        if not v.endswith('/'):
            return f"{v}/"
        return v

    @property
    def full_url(self):
        return f'{self.base_url}{self.endpoint}'

    def _include_auth_info(self):
        if self.token:
            self.headers['Authorization'] = f'Token {self.token.get_secret_value()}'

        if self.project:
            self.params['project'] = self.project

    def post(self) -> WatersyncResponse:
        self._include_auth_info()

        response = requests.post(
            self.full_url, json=self.data, params=self.params, headers=self.headers)

        return WatersyncResponse(response=response)

    def get(self) -> WatersyncResponse:
        self._include_auth_info()

        response = requests.get(
            self.full_url, params=self.params, headers=self.headers)

        return WatersyncResponse(response=response)

    def delete(self):
        self._include_auth_info()

        return NotImplementedError("DELETE method not implemented yet.")

    def patch(self):
        self._include_auth_info()

        return NotImplementedError("PATCH method not implemented yet.")


class WatersyncClient(BaseModel):
    """
    Stores the basic information needed to interact with the API.

    Attributes:
        base_url (str): The base url of the API.
        project (str): The project name.
        token (SecretStr): The token needed to authenticate with the API.

    Methods:
        login: Obtain a token from the API.
    """
    base_url: str
    project: str
    token: Optional[SecretStr] = field(default=None, repr=False)

    def login(self,
              email: Optional[EmailStr] = None,
              password: Optional[str] = None):
        """
        Obtain a token from the API.

        Args:
            email (str): The email of the user. If not provided a prompt will appear. Default is None.
            password (str): The password of the user. If not provided a prompt will appear. Default is None.

        Returns:
            None
        """

        email = input("Enter your email: ") if not email else email
        password = getpass(
            "Enter your password: ") if not password else password

        request = WatersyncRequest(
            base_url=self.base_url,
            endpoint=API_ENDPOINTS['login'],
            data={'email': email, 'password': password}
        )

        response = request.post()

        if response.status_code == 200 and isinstance(response.content, dict):
            self.token = SecretStr(response.content['token'])
            print("Login successful.")
        else:
            raise Exception(response.fail)
