import logging
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
from django.conf import settings

logger = logging.getLogger('services')


class GetFeeBr:
    def __init__(self):
        self.__base_url = "https://brasilapi.com.br/api/taxas/v1"
        self.__timeout = getattr(settings, 'API_TIMEOUT', 10)

    def get_taxa(self, sigla):
        """
        Busca uma taxa economica na BrasilAPI.

        Args:
            sigla: Sigla da taxa (ex: SELIC, CDI, IPCA)

        Returns:
            dict: Dados da taxa ou dict com valor padrao em caso de erro
        """
        logger.info(f"Buscando taxa: {sigla}")

        try:
            response = requests.get(
                url=f"{self.__base_url}/{sigla}",
                timeout=self.__timeout
            )
            response.raise_for_status()

            data = response.json()
            logger.info(f"Taxa {sigla} obtida com sucesso: {data.get('valor', 'N/A')}")
            return data

        except Timeout:
            logger.error(f"Timeout ao buscar taxa {sigla}")
            return self._default_response(sigla)
        except ConnectionError:
            logger.error(f"Erro de conexao ao buscar taxa {sigla}")
            return self._default_response(sigla)
        except RequestException as e:
            logger.error(f"Erro de requisicao ao buscar taxa {sigla}: {str(e)}")
            return self._default_response(sigla)
        except Exception as e:
            logger.exception(f"Erro inesperado ao buscar taxa {sigla}: {str(e)}")
            return self._default_response(sigla)

    def _default_response(self, sigla):
        """Retorna uma resposta padrao quando a API falha."""
        return {
            "nome": sigla,
            "valor": None,
            "error": True
        }
