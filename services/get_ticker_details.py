import requests
from django.conf import settings


class Get_ticker_data:
    def __init__(self):
        self.__base_url = "https://brapi.dev/api/quote"
        self.__base_token = settings.BRAPI_TOKEN

    def get_ticker(self, code_ticekr):
        response = requests.get(
            url=f"{self.__base_url}/{code_ticekr}?token={self.__base_token}"
        )

        return response.json().get("results")[0]

    def get_ticker_dividends(self, code_ticker):
        response = requests.get(
            url=f"{self.__base_url}/{code_ticker}?fundamental=true&dividends=true&token={self.__base_token}"
        )

        return response.json()
