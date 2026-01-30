# Cache Configuration

Este documento descreve a configuracao de cache do InvestSIO.

## Visao Geral

O sistema utiliza cache para melhorar a performance das consultas ao banco de dados, especialmente nas funcoes de metricas que sao chamadas frequentemente no dashboard.

## Configuracao

### Desenvolvimento (LocMemCache)

Em desenvolvimento, o cache utiliza `LocMemCache` (memoria local), que nao requer nenhuma configuracao adicional.

```python
# app/settings/dev.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,
    }
}
```

### Producao (Redis)

Em producao, o cache utiliza Redis para melhor performance e persistencia.

```python
# app/settings/base.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_URL', default='redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'investsio',
        'TIMEOUT': 300,
    }
}
```

**Variaveis de ambiente necessarias:**
- `REDIS_URL`: URL de conexao com o Redis (ex: `redis://127.0.0.1:6379/1`)

## Tempos de Cache (TTL)

O sistema define tres niveis de TTL:

| Constante | Tempo | Uso |
|-----------|-------|-----|
| `CACHE_TTL_SHORT` | 60s | Dados que mudam frequentemente |
| `CACHE_TTL_MEDIUM` | 300s (5 min) | Metricas do dashboard |
| `CACHE_TTL_LONG` | 3600s (1 hora) | Dados estaticos |

## Funcoes com Cache

As seguintes funcoes em `app/metrics.py` utilizam cache:

| Funcao | Chave de Cache | TTL |
|--------|----------------|-----|
| `get_total_invested()` | `total_invested` | 5 min |
| `get_total_applied_by_currency()` | `total_applied_by_currency` | 5 min |
| `get_total_applied_by_broker()` | `total_applied_by_broker` | 5 min |
| `chart_total_category_invested()` | `chart_category_invested` | 5 min |
| `get_total_category_invested(category)` | `category_invested_{category}` | 5 min |
| `get_total_dividends_category(category)` | `dividends_category_{category}` | 5 min |
| `get_applied_value(currency)` | `applied_value_{currency}` | 5 min |

## Invalidacao de Cache

### Quando Invalidar

O cache deve ser invalidado quando:
- Um novo Inflow e criado/atualizado/deletado
- Um novo Outflow e criado/atualizado/deletado
- Um novo Dividend e criado/atualizado/deletado

### Como Invalidar

Use a funcao `invalidate_metrics_cache()` disponivel em `app/metrics.py`:

```python
from app.metrics import invalidate_metrics_cache

# Apos criar/atualizar/deletar uma transacao
invalidate_metrics_cache()
```

### Exemplo de Uso em Views

```python
from app.metrics import invalidate_metrics_cache

class InflowCreateView(CreateView):
    # ...

    def form_valid(self, form):
        response = super().form_valid(form)
        invalidate_metrics_cache()  # Invalida o cache apos criar
        return response
```

### Exemplo de Uso em Signals

```python
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from inflows.models import Inflow
from app.metrics import invalidate_metrics_cache

@receiver([post_save, post_delete], sender=Inflow)
def invalidate_cache_on_inflow_change(sender, **kwargs):
    invalidate_metrics_cache()
```

## Monitoramento

### Verificar Status do Redis

```bash
redis-cli ping
# Resposta esperada: PONG
```

### Ver Chaves em Cache

```bash
redis-cli keys "investsio:*"
```

### Limpar Todo o Cache

```bash
redis-cli flushdb
```

Ou via Django:

```python
from django.core.cache import cache
cache.clear()
```

## Troubleshooting

### Cache nao funciona em desenvolvimento

Em desenvolvimento, o `LocMemCache` e reiniciado a cada reload do servidor. Isso e normal.

### Redis nao conecta

1. Verifique se o Redis esta rodando: `redis-cli ping`
2. Verifique a variavel `REDIS_URL` no `.env`
3. Verifique se a porta 6379 esta disponivel

### Dados desatualizados

Se os dados parecem desatualizados apos mudancas:
1. Verifique se `invalidate_metrics_cache()` esta sendo chamada
2. Limpe o cache manualmente: `cache.clear()`
