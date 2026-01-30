import logging
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
from django.conf import settings

logger = logging.getLogger('services')


class APIError(Exception):
    """Excecao customizada para erros de API."""
    pass


class Get_ticker_data:
    def __init__(self):
        self.__base_url = "https://brapi.dev/api/quote"
        self.__base_token = settings.BRAPI_TOKEN
        self.__timeout = getattr(settings, 'API_TIMEOUT', 10)

    def get_ticker(self, code_ticker):
        """
        Busca dados de um ticker na BrAPI.

        Args:
            code_ticker: Codigo do ticker (ex: PETR4)

        Returns:
            dict: Dados do ticker ou None em caso de erro
        """
        logger.info(f"Buscando dados do ticker: {code_ticker}")

        try:
            response = requests.get(
                url=f"{self.__base_url}/{code_ticker}?token={self.__base_token}",
                timeout=self.__timeout
            )
            response.raise_for_status()

            data = response.json()
            results = data.get("results")

            if not results:
                logger.warning(f"Nenhum resultado encontrado para ticker: {code_ticker}")
                return None

            logger.info(f"Dados do ticker {code_ticker} obtidos com sucesso")
            return results[0]

        except Timeout:
            logger.error(f"Timeout ao buscar ticker {code_ticker}")
            return None
        except ConnectionError:
            logger.error(f"Erro de conexao ao buscar ticker {code_ticker}")
            return None
        except RequestException as e:
            logger.error(f"Erro de requisicao ao buscar ticker {code_ticker}: {str(e)}")
            return None
        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"Erro ao processar resposta do ticker {code_ticker}: {str(e)}")
            return None
        except Exception as e:
            logger.exception(f"Erro inesperado ao buscar ticker {code_ticker}: {str(e)}")
            return None

    def get_ticker_dividends(self, code_ticker):
        """
        Busca dados de dividendos de um ticker na BrAPI.

        Args:
            code_ticker: Codigo do ticker (ex: PETR4)

        Returns:
            dict: Dados de dividendos ou None em caso de erro
        """
        logger.info(f"Buscando dividendos do ticker: {code_ticker}")

        try:
            response = requests.get(
                url=f"{self.__base_url}/{code_ticker}?fundamental=true&dividends=true&token={self.__base_token}",
                timeout=self.__timeout
            )
            response.raise_for_status()

            data = response.json()
            logger.info(f"Dividendos do ticker {code_ticker} obtidos com sucesso")
            return data

        except Timeout:
            logger.error(f"Timeout ao buscar dividendos do ticker {code_ticker}")
            return None
        except ConnectionError:
            logger.error(f"Erro de conexao ao buscar dividendos do ticker {code_ticker}")
            return None
        except RequestException as e:
            logger.error(f"Erro de requisicao ao buscar dividendos do ticker {code_ticker}: {str(e)}")
            return None
        except Exception as e:
            logger.exception(f"Erro inesperado ao buscar dividendos do ticker {code_ticker}: {str(e)}")
            return None
