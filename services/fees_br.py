import requests


class GetFeeBr():
    def __init__(self):
        self.__base_url = "https://brasilapi.com.br/api/taxas/v1"

    def get_taxa(self, sigla):
        response = requests.get(
            url=f"{self.__base_url}/{sigla}"
        )
        return response.json()
