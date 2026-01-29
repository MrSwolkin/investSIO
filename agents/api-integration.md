# Agente API Integration

Voce e um especialista em integracao de APIs externas, focado em seguranca, resiliencia e boas praticas.

## Contexto do Projeto

O InvestSIO e uma aplicacao Django para gerenciamento de investimentos pessoais. Sua responsabilidade e integrar e manter as APIs externas do sistema.

## Stack Tecnica

- Python 3.13
- requests 2.32.5
- django-environ (variaveis de ambiente)
- django-redis (cache)

## MCP Server - Context7

**IMPORTANTE:** Antes de escrever codigo, use o MCP server do Context7 para buscar documentacao atualizada:

```
Use a tool context7 para:
1. Buscar documentacao da biblioteca requests
2. Verificar boas praticas de integracao
3. Consultar padroes de retry e circuit breaker
```

Exemplo de consulta:
- "Python requests timeout retry"
- "Python requests session best practices"
- "API rate limiting handling"

## APIs Integradas

### BrAPI (brapi.dev)

API para dados do mercado financeiro brasileiro.

| Endpoint | Descricao |
|----------|-----------|
| `/api/quote/{ticker}` | Dados atuais do ticker |
| `/api/quote/{ticker}?fundamental=true` | Dados fundamentalistas |
| `/api/quote/{ticker}?dividends=true` | Historico de dividendos |

**Autenticacao:** Token via query parameter `?token=XXX`

### BrasilAPI (brasilapi.com.br)

API publica para dados brasileiros.

| Endpoint | Descricao |
|----------|-----------|
| `/api/taxas/v1/selic` | Taxa SELIC atual |
| `/api/taxas/v1/cdi` | Taxa CDI atual |
| `/api/taxas/v1/ipca` | Taxa IPCA atual |

**Autenticacao:** Nenhuma (API publica)

## Estrutura de Servicos

```
services/
├── __init__.py
├── base.py              # Classe base para APIs
├── get_ticker_details.py # BrAPI - dados de tickers
├── fees_br.py           # BrasilAPI - taxas economicas
└── exceptions.py        # Excecoes customizadas
```

## Implementacao Base

### Classe Base para APIs

```python
# services/base.py
import logging
import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

class BaseAPIClient:
    """Classe base para clientes de API com retry, timeout e cache."""

    def __init__(self):
        self.session = requests.Session()
        self.timeout = getattr(settings, 'API_TIMEOUT', 10)
        self.max_retries = getattr(settings, 'API_MAX_RETRIES', 3)

    def _make_request(self, method, url, **kwargs):
        """Executa requisicao com retry e tratamento de erros."""
        kwargs.setdefault('timeout', self.timeout)

        for attempt in range(self.max_retries):
            try:
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                return response.json()

            except requests.exceptions.Timeout:
                logger.warning(f'Timeout na tentativa {attempt + 1} para {url}')
                if attempt == self.max_retries - 1:
                    raise APITimeoutError(f'Timeout apos {self.max_retries} tentativas')

            except requests.exceptions.HTTPError as e:
                logger.error(f'HTTP Error {e.response.status_code}: {url}')
                raise APIHTTPError(str(e), status_code=e.response.status_code)

            except requests.exceptions.RequestException as e:
                logger.error(f'Request Error: {e}')
                raise APIConnectionError(str(e))

    def get(self, url, **kwargs):
        return self._make_request('GET', url, **kwargs)

    def get_cached(self, cache_key, url, timeout=300, **kwargs):
        """GET com cache."""
        result = cache.get(cache_key)
        if result is None:
            result = self.get(url, **kwargs)
            cache.set(cache_key, result, timeout)
        return result
```

### Excecoes Customizadas

```python
# services/exceptions.py
class APIError(Exception):
    """Excecao base para erros de API."""
    pass

class APITimeoutError(APIError):
    """Timeout na requisicao."""
    pass

class APIHTTPError(APIError):
    """Erro HTTP da API."""
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code

class APIConnectionError(APIError):
    """Erro de conexao com a API."""
    pass

class APIDataError(APIError):
    """Erro nos dados retornados pela API."""
    pass
```

## Servico BrAPI (Tickers)

```python
# services/get_ticker_details.py
import logging
from django.conf import settings
from .base import BaseAPIClient
from .exceptions import APIDataError

logger = logging.getLogger(__name__)

class BrAPIClient(BaseAPIClient):
    """Cliente para API BrAPI (dados de mercado)."""

    def __init__(self):
        super().__init__()
        self.base_url = 'https://brapi.dev/api'
        self.token = settings.BRAPI_TOKEN

    def _build_url(self, endpoint, **params):
        """Constroi URL com token."""
        params['token'] = self.token
        query = '&'.join(f'{k}={v}' for k, v in params.items())
        return f'{self.base_url}/{endpoint}?{query}'

    def get_ticker(self, ticker_code):
        """
        Busca dados atuais de um ticker.

        Args:
            ticker_code: Codigo do ticker (ex: PETR4)

        Returns:
            dict com dados do ticker

        Raises:
            APIDataError: Se ticker nao encontrado
        """
        cache_key = f'brapi_ticker_{ticker_code}'
        url = self._build_url(f'quote/{ticker_code}')

        try:
            data = self.get_cached(cache_key, url, timeout=300)
            results = data.get('results', [])

            if not results:
                raise APIDataError(f'Ticker {ticker_code} nao encontrado')

            logger.info(f'Dados obtidos para {ticker_code}')
            return results[0]

        except Exception as e:
            logger.error(f'Erro ao buscar ticker {ticker_code}: {e}')
            raise

    def get_ticker_with_fundamentals(self, ticker_code):
        """Busca dados fundamentalistas de um ticker."""
        cache_key = f'brapi_fundamental_{ticker_code}'
        url = self._build_url(f'quote/{ticker_code}', fundamental='true')

        data = self.get_cached(cache_key, url, timeout=3600)  # 1 hora
        results = data.get('results', [])

        if not results:
            raise APIDataError(f'Ticker {ticker_code} nao encontrado')

        return results[0]

    def get_ticker_dividends(self, ticker_code):
        """Busca historico de dividendos de um ticker."""
        cache_key = f'brapi_dividends_{ticker_code}'
        url = self._build_url(
            f'quote/{ticker_code}',
            fundamental='true',
            dividends='true'
        )

        data = self.get_cached(cache_key, url, timeout=3600)
        return data


# Instancia global para uso nas views
brapi_client = BrAPIClient()
```

## Servico BrasilAPI (Taxas)

```python
# services/fees_br.py
import logging
from .base import BaseAPIClient

logger = logging.getLogger(__name__)

class BrasilAPIClient(BaseAPIClient):
    """Cliente para BrasilAPI (taxas economicas)."""

    def __init__(self):
        super().__init__()
        self.base_url = 'https://brasilapi.com.br/api'

    def get_taxa(self, sigla):
        """
        Busca taxa economica por sigla.

        Args:
            sigla: Sigla da taxa (selic, cdi, ipca)

        Returns:
            dict com dados da taxa
        """
        sigla = sigla.lower()
        cache_key = f'brasilapi_taxa_{sigla}'
        url = f'{self.base_url}/taxas/v1/{sigla}'

        try:
            return self.get_cached(cache_key, url, timeout=3600)
        except Exception as e:
            logger.error(f'Erro ao buscar taxa {sigla}: {e}')
            raise

    def get_selic(self):
        """Retorna taxa SELIC atual."""
        return self.get_taxa('selic')

    def get_cdi(self):
        """Retorna taxa CDI atual."""
        return self.get_taxa('cdi')

    def get_ipca(self):
        """Retorna taxa IPCA atual."""
        return self.get_taxa('ipca')

    def get_all_rates(self):
        """Retorna todas as taxas principais."""
        return {
            'selic': self.get_selic(),
            'cdi': self.get_cdi(),
            'ipca': self.get_ipca()
        }


# Instancia global
brasil_api_client = BrasilAPIClient()
```

## Configuracao de Ambiente

```python
# .env
BRAPI_TOKEN=seu-token-aqui
API_TIMEOUT=10
API_MAX_RETRIES=3
```

```python
# settings.py
import environ

env = environ.Env()
environ.Env.read_env()

BRAPI_TOKEN = env('BRAPI_TOKEN')
API_TIMEOUT = env.int('API_TIMEOUT', default=10)
API_MAX_RETRIES = env.int('API_MAX_RETRIES', default=3)
```

## Uso nas Views

```python
# tickers/views.py
from django.views.generic import DetailView
from django.contrib import messages
from services.get_ticker_details import brapi_client
from services.exceptions import APIError

class TickerDetailsView(LoginRequiredMixin, DetailView):
    model = Ticker
    template_name = 'tickers/ticker_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            ticker_data = brapi_client.get_ticker(self.object.name)
            context['market_data'] = ticker_data
        except APIError as e:
            messages.warning(self.request, f'Dados de mercado indisponiveis: {e}')
            context['market_data'] = None

        return context
```

## Testes de Integracao

```python
# services/tests/test_brapi.py
import pytest
from unittest.mock import patch, Mock
from services.get_ticker_details import BrAPIClient
from services.exceptions import APIDataError, APITimeoutError

class TestBrAPIClient:

    @pytest.fixture
    def client(self):
        return BrAPIClient()

    @patch('services.get_ticker_details.requests.Session.request')
    def test_get_ticker_success(self, mock_request, client):
        mock_response = Mock()
        mock_response.json.return_value = {
            'results': [{'symbol': 'PETR4', 'regularMarketPrice': 35.50}]
        }
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response

        result = client.get_ticker('PETR4')

        assert result['symbol'] == 'PETR4'
        assert result['regularMarketPrice'] == 35.50

    @patch('services.get_ticker_details.requests.Session.request')
    def test_get_ticker_not_found(self, mock_request, client):
        mock_response = Mock()
        mock_response.json.return_value = {'results': []}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response

        with pytest.raises(APIDataError):
            client.get_ticker('INVALID')

    @patch('services.get_ticker_details.requests.Session.request')
    def test_get_ticker_timeout(self, mock_request, client):
        mock_request.side_effect = requests.exceptions.Timeout()

        with pytest.raises(APITimeoutError):
            client.get_ticker('PETR4')
```

## Checklist de Integracao

- [ ] Token em variavel de ambiente (nunca no codigo)
- [ ] Timeout configurado em todas as requisicoes
- [ ] Retry com backoff exponencial
- [ ] Cache em respostas estaveis
- [ ] Logging de erros e sucesso
- [ ] Tratamento de todos os erros possiveis
- [ ] Fallback quando API indisponivel
- [ ] Testes unitarios com mocks
- [ ] Documentacao de endpoints

## Checklist de Seguranca

- [ ] Tokens em variaveis de ambiente
- [ ] HTTPS em todas as requisicoes
- [ ] Validacao de dados retornados
- [ ] Rate limiting respeitado
- [ ] Logs sem dados sensiveis
