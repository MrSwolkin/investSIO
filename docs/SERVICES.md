# Services

Documentacao dos servicos externos integrados ao projeto.

## Visao Geral

O projeto integra com duas APIs externas:

| Servico | Arquivo | Descricao |
|---------|---------|-----------|
| BrasilAPI | `services/fees_br.py` | Taxas economicas brasileiras |
| BrAPI | `services/get_ticker_details.py` | Dados de tickers da bolsa |

---

## BrasilAPI - Taxas Economicas

**Arquivo:** `services/fees_br.py`

**Classe:** `GetFeeBr`

### Metodo: get_taxa(sigla)

Consulta taxas economicas na BrasilAPI.

**Parametros:**
- `sigla` (str): Codigo da taxa (IPCA, SELIC, CDI)

**Retorno:** JSON com dados da taxa

**Exemplo de uso:**

```python
from services.fees_br import GetFeeBr

api = GetFeeBr()
ipca = api.get_taxa("IPCA")
selic = api.get_taxa("SELIC")
cdi = api.get_taxa("CDI")
```

**URL base:** `https://brasilapi.com.br/api/taxas/v1/{sigla}`

**Resposta exemplo:**

```json
{
  "nome": "IPCA",
  "valor": 4.23,
  "dataAtualizacao": "2024-01-15"
}
```

---

## BrAPI - Dados de Tickers

**Arquivo:** `services/get_ticker_details.py`

**Classe:** `Get_ticker_data`

### Metodo: get_ticker(code_ticker)

Busca dados atuais de um ticker.

**Parametros:**
- `code_ticker` (str): Codigo do ticker (ex: MGLU3, BBAS3)

**Retorno:** JSON com dados do ticker

**Dados retornados:**
- `regularMarketPrice` - Preco atual
- `logourl` - URL do icone da empresa
- `longName` - Nome completo da empresa

**Exemplo de uso:**

```python
from services.get_ticker_details import Get_ticker_data

api = Get_ticker_data()
data = api.get_ticker("MGLU3")
preco = data['results'][0]['regularMarketPrice']
logo = data['results'][0]['logourl']
nome = data['results'][0]['longName']
```

### Metodo: get_ticker_dividends(code_ticker)

Busca historico de dividendos de um ticker.

**Parametros:**
- `code_ticker` (str): Codigo do ticker

**Retorno:** JSON com dividendos do ticker

**Exemplo de uso:**

```python
from services.get_ticker_details import Get_ticker_data

api = Get_ticker_data()
dividends = api.get_ticker_dividends("BBAS3")
```

**URL base:** `https://brapi.dev/api/quote/{ticker}`

**Headers necessarios:**
- `Authorization: Bearer {token}`

---

## Uso nas Views

### Dashboard (app/views.py)

```python
from services.fees_br import GetFeeBr

def home(request):
    api = GetFeeBr()
    ipca_data = api.get_taxa("IPCA")
    selic_data = api.get_taxa("SELIC")
    cdi_data = api.get_taxa("CDI")

    context = {
        'ipca': ipca_data['valor'],
        'selic': selic_data['valor'],
        'cdi': cdi_data['valor'],
    }
    return render(request, 'home.html', context)
```

### Detalhes do Ticker (tickers/views.py)

```python
from services.get_ticker_details import Get_ticker_data

class TickerDetailsView(DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        api = Get_ticker_data()
        ticker_data = api.get_ticker(self.object.name)

        context['price'] = ticker_data['results'][0]['regularMarketPrice']
        context['ticker_icon'] = ticker_data['results'][0]['logourl']
        context['ticker_long_name'] = ticker_data['results'][0]['longName']

        return context
```

---

## Tratamento de Erros

As APIs podem falhar por diversos motivos. Recomenda-se tratar erros:

```python
import requests

try:
    response = api.get_ticker("MGLU3")
    preco = response['results'][0]['regularMarketPrice']
except requests.RequestException:
    preco = None  # Falha na requisicao
except (KeyError, IndexError):
    preco = None  # Dados nao encontrados
```

---

## Limites e Consideracoes

### BrasilAPI
- API publica, sem necessidade de autenticacao
- Dados atualizados periodicamente
- Sem limite de requisicoes documentado

### BrAPI
- Requer token de autenticacao
- Plano gratuito tem limite de requisicoes
- Dados em tempo real durante pregao
