# Melhorias de Backend

Documento com analise completa do backend e recomendacoes de melhorias seguindo as melhores praticas do mercado.

---

## Sumario de Problemas

| Severidade | Quantidade | Status |
|------------|------------|--------|
| Critico | 15 | Pendente |
| Alto | 12 | Pendente |
| Medio | 10 | Pendente |

---

## 1. Seguranca

### 1.1 Configuracoes Expostas (CRITICO)

**Problema:** `app/settings.py` com configuracoes sensiveis expostas.

| Item | Status Atual | Risco |
|------|--------------|-------|
| `DEBUG` | `True` hardcoded | Critico |
| `SECRET_KEY` | Exposta no codigo | Critico |
| `ALLOWED_HOSTS` | Lista vazia `[]` | Alto |

**Solucao:**

```python
# Instalar django-environ
# pip install django-environ

import environ

env = environ.Env()
environ.Env.read_env()

DEBUG = env.bool('DEBUG', default=False)
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
```

**Criar arquivo `.env`:**
```env
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

### 1.2 Token de API Exposto (CRITICO)

**Arquivo:** `services/get_ticker_details.py`

**Problema:** Token da BrAPI hardcoded no codigo.

```python
# ATUAL (ERRADO)
self.__base_token = "2SqXLtCk9gzmBiTNtm1iz8"

# CORRETO
import os
self.__base_token = os.environ.get('BRAPI_TOKEN')
```

---

### 1.3 Autenticacao e Autorizacao (CRITICO)

**Problema:** Todas as views sao publicas, sem verificacao de login ou permissoes.

**Solucao:** Adicionar `LoginRequiredMixin` em todas as CBVs.

```python
# ATUAL
class BrokerListView(ListView):
    model = Broker

# CORRETO
from django.contrib.auth.mixins import LoginRequiredMixin

class BrokerListView(LoginRequiredMixin, ListView):
    model = Broker
    login_url = '/login/'
```

**Views que precisam de protecao:**
- [ ] BrokerListView, BrokerCreateView, BrokerUpdateView, BrokerDeleteView
- [ ] TickerListView, TickerCreateView, TickerUpdateView, TickerDeleteView
- [ ] InflowListView, InflowCreateView, InflowUpdateView, InflowDeleteView
- [ ] OutflowListView, OutflowCreateView, OutflowUpdateView, OutflowDeleteView
- [ ] DividendListView, DividendCreateView, DividendUpdateView, DividendDeleteView
- [ ] home(), negociations()

---

### 1.4 Validacao de Input (ALTO)

**Problema:** Parametros GET usados diretamente em queries sem validacao.

**Arquivo:** `dividends/views.py`

```python
# ATUAL (VULNERAVEL)
ticker = self.request.GET.get("ticker")
queryset = queryset.filter(ticker__name=ticker)

# CORRETO
from django.core.exceptions import ValidationError

ticker = self.request.GET.get("ticker")
if ticker:
    # Validar que existe
    if not Ticker.objects.filter(name=ticker).exists():
        raise Http404("Ticker nao encontrado")
    queryset = queryset.filter(ticker__name=ticker)
```

---

### 1.5 Configuracoes SSL/HTTPS (MEDIO)

**Adicionar em settings.py para producao:**

```python
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

---

## 2. Estrutura de Codigo

### 2.1 Separacao de Ambientes (CRITICO)

**Problema:** Unico arquivo settings.py para todos os ambientes.

**Solucao:** Criar estrutura de settings modular.

```
app/
├── settings/
│   ├── __init__.py
│   ├── base.py      # Configuracoes comuns
│   ├── dev.py       # Desenvolvimento
│   └── prod.py      # Producao
```

**base.py:**
```python
import environ
from pathlib import Path

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [...]
MIDDLEWARE = [...]
# Configuracoes comuns
```

**dev.py:**
```python
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

**prod.py:**
```python
from .base import *

DEBUG = False
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
```

---

### 2.2 Violacao do Principio DRY (ALTO)

**Arquivo:** `app/metrics.py`

**Problema:** Funcoes com logica duplicada.

**Solucao:** Criar funcoes helper reutilizaveis.

```python
# CRIAR: app/utils/aggregations.py

def aggregate_by_currency(queryset, date_field='date', value_field='total_price'):
    """Helper para agregacoes por moeda."""
    return queryset.values(
        f'{date_field}__year',
        f'{date_field}__month'
    ).annotate(total=Sum(value_field))
```

---

### 2.3 App Vazio (MEDIO)

**Problema:** App `portifolio/` existe mas esta vazio.

**Solucao:** Remover app nao utilizado ou implementar funcionalidade.

```bash
# Remover do INSTALLED_APPS em settings.py
# Deletar pasta portifolio/
```

---

## 3. Models

### 3.1 Falta de Indices (CRITICO)

**Problema:** Nenhum indice definido em ForeignKeys de alta utilizacao.

**Solucao:** Adicionar `db_index=True` em campos frequentemente filtrados.

```python
# inflows/models.py
class Inflow(models.Model):
    ticker = models.ForeignKey(
        Ticker,
        on_delete=models.PROTECT,
        related_name="inflows",
        db_index=True  # ADICIONAR
    )
    broker = models.ForeignKey(
        Broker,
        on_delete=models.PROTECT,
        null=True,
        db_index=True  # ADICIONAR
    )
    date = models.DateField(db_index=True)  # ADICIONAR

    class Meta:
        indexes = [
            models.Index(fields=['ticker', 'date']),
            models.Index(fields=['date']),
        ]
```

**Aplicar em:**
- [ ] `Inflow.ticker`, `Inflow.broker`, `Inflow.date`
- [ ] `Outflow.ticker`, `Outflow.broker`, `Outflow.date`
- [ ] `Dividend.ticker`, `Dividend.date`
- [ ] `Ticker.category`, `Ticker.currency`

---

### 3.2 Validacoes Ausentes (CRITICO)

**Problema:** Models sem validacoes de negocio.

**Solucao:** Adicionar metodo `clean()` e validators.

```python
# inflows/models.py
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

class Inflow(models.Model):
    quantity = models.IntegerField(
        validators=[MinValueValidator(1, "Quantidade deve ser maior que zero")]
    )
    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01, "Preco deve ser maior que zero")]
    )
    date = models.DateField()

    def clean(self):
        super().clean()
        if self.date and self.date > timezone.now().date():
            raise ValidationError({'date': 'Data nao pode ser futura'})

        if self.tax and self.tax < 0:
            raise ValidationError({'tax': 'Taxa nao pode ser negativa'})
```

---

### 3.3 Query Pesada no save() (CRITICO)

**Arquivo:** `dividends/models.py`

**Problema:** Query executada dentro do metodo `save()`.

```python
# ATUAL (PROBLEMA)
def save(self, *args, **kwargs):
    if not self.quantity_quote:
        self.quantity_quote = Inflow.objects.filter(...).aggregate(...)
```

**Solucao:** Mover logica para view ou signal.

```python
# CORRETO - Usar signal ou calcular na view
# dividends/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=Dividend)
def calculate_quantity_quote(sender, instance, **kwargs):
    if not instance.quantity_quote:
        instance.quantity_quote = calculate_quote_for_date(
            instance.ticker,
            instance.date
        )
```

---

### 3.4 Typos em Related Names (ALTO) - CORRIGIDO

**Arquivo:** `dividends/models.py`

**Status:** ✅ Corrigido

```python
# CORRIGIDO
ticker = models.ForeignKey(Ticker, related_name="dividends")
```

**Nota:** Migration criada em `dividends/migrations/0009_fix_related_name_typo.py`.

---

### 3.5 Campos Denormalizados (MEDIO)

**Problema:** `total_price` calculado e armazenado.

**Alternativa:** Usar property calculada.

```python
class Inflow(models.Model):
    # Remover campo total_price do model

    @property
    def total_price(self):
        return self.cost_price * self.quantity
```

**Ou:** Manter denormalizado mas documentar motivo (performance).

---

## 4. Views

### 4.1 N+1 Queries (CRITICO)

**Problema:** Queries sem otimizacao em loops.

**Arquivo:** `app/metrics.py`, `tickers/views.py`

**Solucao:** Usar `select_related()` e `prefetch_related()`.

```python
# ATUAL
inflows = Inflow.objects.filter(ticker=self.object)

# CORRETO
inflows = Inflow.objects.filter(ticker=self.object).select_related(
    'ticker',
    'ticker__category',
    'ticker__currency',
    'broker',
    'broker__currency'
)
```

**Aplicar em:**
- [ ] `InflowListView.get_queryset()`
- [ ] `OutflowListView.get_queryset()`
- [ ] `DividendListView.get_queryset()`
- [ ] `TickerDetailsView.get_context_data()`
- [ ] `negociations()` view

---

### 4.2 Paginacao Ausente (CRITICO)

**Problema:** ListViews carregam todos os registros.

**Solucao:** Adicionar paginacao.

```python
class InflowListView(LoginRequiredMixin, ListView):
    model = Inflow
    paginate_by = 25  # ADICIONAR
    ordering = ['-date']
```

**No template:**
```django
{% if page_obj.has_other_pages %}
<nav>
    <ul class="pagination">
        {% if page_obj.has_previous %}
        <li><a href="?page={{ page_obj.previous_page_number }}">Anterior</a></li>
        {% endif %}
        <li>Pagina {{ page_obj.number }} de {{ page_obj.paginator.num_pages }}</li>
        {% if page_obj.has_next %}
        <li><a href="?page={{ page_obj.next_page_number }}">Proxima</a></li>
        {% endif %}
    </ul>
</nav>
{% endif %}
```

---

### 4.3 Tratamento de Erros (CRITICO)

**Problema:** Chamadas de API sem tratamento de erro.

**Arquivo:** `services/get_ticker_details.py`

```python
# ATUAL (SEM TRATAMENTO)
def get_ticker(self, code_ticker):
    response = requests.get(url, headers=headers)
    return response.json()

# CORRETO
import logging
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

def get_ticker(self, code_ticker):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        logger.error(f"Erro ao buscar ticker {code_ticker}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Erro ao parsear JSON: {e}")
        return None
```

---

### 4.4 Processamento em Memoria (ALTO)

**Arquivo:** `app/views.py`

**Problema:** Todos os registros carregados para ordenacao.

```python
# ATUAL (PROBLEMA)
transactions = sorted(chain(inflow, outflow), key=lambda obj: obj.date)

# SOLUCAO 1: Union query
from django.db.models import Value, CharField

inflows = Inflow.objects.annotate(
    type=Value('compra', CharField())
).values('id', 'date', 'ticker__name', 'total_price', 'type')

outflows = Outflow.objects.annotate(
    type=Value('venda', CharField())
).values('id', 'date', 'ticker__name', 'total_price', 'type')

transactions = inflows.union(outflows).order_by('-date')[:50]
```

---

### 4.5 Typo em Nome de View (MEDIO)

**Arquivo:** `outflows/views.py`

```python
# CORRIGIDO
class OutflowListView(ListView):  # Typo corrigido
```

---

## 5. Performance

### 5.1 Cache (CRITICO)

**Problema:** Nenhum cache configurado.

**Solucao:** Configurar Redis como cache.

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

**Uso em views:**
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache 15 minutos
def home(request):
    ...
```

**Uso em metricas:**
```python
from django.core.cache import cache

def get_total_invested():
    cache_key = 'total_invested'
    result = cache.get(cache_key)
    if result is None:
        result = Inflow.objects.aggregate(total=Sum('total_price'))
        cache.set(cache_key, result, 60 * 60)  # 1 hora
    return result
```

---

### 5.2 Logging (ALTO)

**Problema:** Nenhum logging configurado.

**Solucao:** Adicionar configuracao de logging.

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

---

### 5.3 Database (ALTO)

**Problema:** SQLite em producao.

**Solucao:** Migrar para PostgreSQL.

```python
# settings/prod.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
    }
}
```

---

## 6. Testes

### 6.1 Cobertura Zero (CRITICO)

**Problema:** Nenhum teste no projeto.

**Solucao:** Implementar testes com pytest.

```bash
pip install pytest pytest-django pytest-cov
```

**pytest.ini:**
```ini
[pytest]
DJANGO_SETTINGS_MODULE = app.settings.dev
python_files = tests.py test_*.py *_tests.py
addopts = --cov=. --cov-report=html
```

**Exemplo de teste:**
```python
# brokers/tests.py
import pytest
from django.urls import reverse
from .models import Broker, Currency

@pytest.mark.django_db
class TestBrokerModel:
    def test_create_broker(self):
        currency = Currency.objects.create(code='BRL', name='Real')
        broker = Broker.objects.create(
            name='XP Investimentos',
            currency=currency
        )
        assert broker.name == 'XP Investimentos'
        assert str(broker) == 'XP Investimentos'

@pytest.mark.django_db
class TestBrokerViews:
    def test_list_view(self, client, django_user_model):
        user = django_user_model.objects.create_user(
            username='test', password='test123'
        )
        client.login(username='test', password='test123')
        response = client.get(reverse('broker_list'))
        assert response.status_code == 200
```

---

## 7. API REST

### 7.1 Sem API REST (MEDIO)

**Problema:** Projeto sem API REST.

**Solucao:** Implementar Django REST Framework.

```bash
pip install djangorestframework
```

```python
# settings.py
INSTALLED_APPS = [
    ...
    'rest_framework',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
}
```

**Exemplo de serializer:**
```python
# brokers/serializers.py
from rest_framework import serializers
from .models import Broker

class BrokerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broker
        fields = ['id', 'name', 'account_number', 'country', 'currency']
```

---

## 8. Signals

### 8.1 Signals sem Registro (ALTO)

**Problema:** Signals nao registrados em `apps.py`.

**Solucao:** Registrar signals corretamente.

```python
# inflows/apps.py
from django.apps import AppConfig

class InflowsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inflows'

    def ready(self):
        import inflows.signals  # Importar signals
```

---

## 9. Checklist de Melhorias

### Fase 1: Seguranca (Prioridade Maxima)

- [ ] Mover credenciais para `.env`
- [ ] Instalar `django-environ`
- [ ] Criar estrutura de settings (base/dev/prod)
- [ ] Adicionar `LoginRequiredMixin` em todas as views
- [ ] Validar inputs em GET parameters
- [ ] Configurar HTTPS para producao

### Fase 2: Performance (Prioridade Alta)

- [ ] Adicionar indices em ForeignKeys
- [ ] Implementar `select_related()`/`prefetch_related()`
- [ ] Adicionar paginacao em ListViews
- [ ] Configurar cache com Redis
- [ ] Otimizar queries em `metrics.py`
- [ ] Remover processamento em memoria

### Fase 3: Qualidade (Prioridade Media)

- [ ] Adicionar validacoes em models
- [ ] Implementar testes com pytest
- [ ] Configurar logging
- [ ] Corrigir typos (OuflowListView, dividens)
- [ ] Adicionar docstrings
- [ ] Remover codigo comentado

### Fase 4: Escalabilidade (Prioridade Baixa)

- [ ] Migrar para PostgreSQL
- [ ] Implementar Celery para tasks
- [ ] Criar API REST com DRF
- [ ] Configurar CI/CD

---

## 10. Dependencias Recomendadas

**Adicionar ao requirements.txt:**

```txt
# Seguranca e Configuracao
django-environ==0.11.2

# Performance
django-redis==5.4.0
redis==5.0.1

# Debug (dev only)
django-debug-toolbar==4.2.0

# Testes
pytest==7.4.3
pytest-django==4.7.0
pytest-cov==4.1.0

# API REST
djangorestframework==3.14.0

# Tasks Assincronas
celery==5.3.4
redis==5.0.1

# Database (producao)
psycopg2-binary==2.9.9

# Validacao
django-cors-headers==4.3.1
```

---

## Referencias

- [Django Security Best Practices](https://docs.djangoproject.com/en/5.0/topics/security/)
- [Django Performance Optimization](https://docs.djangoproject.com/en/5.0/topics/performance/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [pytest-django](https://pytest-django.readthedocs.io/)

---

**Documento criado em:** 29/01/2026
**Ultima atualizacao:** 29/01/2026
