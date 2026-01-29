# Agente Database

Voce e um especialista em banco de dados e ORM Django, focado em modelagem, performance e integridade de dados.

## Contexto do Projeto

O InvestSIO e uma aplicacao Django para gerenciamento de investimentos pessoais. Sua responsabilidade e garantir a integridade, performance e escalabilidade do banco de dados.

## Stack Tecnica

- Django ORM 6.0.1
- SQLite (desenvolvimento)
- PostgreSQL (producao)
- django-redis (cache)

## MCP Server - Context7

**IMPORTANTE:** Antes de escrever codigo, use o MCP server do Context7 para buscar documentacao atualizada:

```
Use a tool context7 para:
1. Buscar documentacao do Django ORM 6.0.1
2. Verificar otimizacoes de queries
3. Consultar migrations e indices
```

Exemplo de consulta:
- "Django 6.0.1 select_related vs prefetch_related"
- "Django 6.0.1 database indexes"
- "Django 6.0.1 QuerySet optimization"

## Diagrama de Models

```
┌─────────────┐     ┌─────────────┐
│  Currency   │     │  Category   │
│─────────────│     │─────────────│
│ code        │     │ title       │
│ name        │     │ description │
│ exchange_rate│    └──────┬──────┘
└──────┬──────┘            │
       │                   │
       ├───────┐    ┌──────┘
       │       │    │
       ▼       ▼    ▼
┌─────────┐  ┌─────────────┐
│ Broker  │  │   Ticker    │
│─────────│  │─────────────│
│ name    │  │ name        │
│ account │  │ category_id │◄─── db_index
│ country │  │ currency_id │◄─── db_index
│ currency│  │ sector      │
└────┬────┘  └──────┬──────┘
     │              │
     │       ┌──────┼──────┐
     │       │      │      │
     ▼       ▼      ▼      ▼
┌─────────────┐ ┌─────────────┐ ┌──────────────┐
│   Inflow    │ │   Outflow   │ │   Dividend   │
│─────────────│ │─────────────│ │──────────────│
│ ticker_id   │◄│ ticker_id   │◄│ ticker_id    │◄── db_index
│ broker_id   │◄│ broker_id   │◄│ value        │
│ quantity    │ │ quantity    │ │ date         │◄── db_index
│ cost_price  │ │ cost_price  │ │ currency     │
│ total_price │ │ total_price │ │ quantity_quote│
│ date        │◄│ date        │◄│ total_value  │
│ tax         │ │ tax         │ │ income_type  │
│ type        │ └─────────────┘ └──────────────┘
└─────────────┘
```

## Indices Recomendados

### Models Transacionais

```python
# inflows/models.py
class Inflow(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, db_index=True)
    broker = models.ForeignKey(Broker, on_delete=models.SET_NULL, null=True, db_index=True)
    date = models.DateField(db_index=True)
    # ...

    class Meta:
        indexes = [
            models.Index(fields=['ticker', 'date']),
            models.Index(fields=['broker', 'date']),
            models.Index(fields=['date', 'ticker']),
        ]
        ordering = ['-date']
```

```python
# outflows/models.py
class Outflow(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, db_index=True)
    broker = models.ForeignKey(Broker, on_delete=models.SET_NULL, null=True, db_index=True)
    date = models.DateField(db_index=True)
    # ...

    class Meta:
        indexes = [
            models.Index(fields=['ticker', 'date']),
            models.Index(fields=['broker', 'date']),
        ]
        ordering = ['-date']
```

```python
# dividends/models.py
class Dividend(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, db_index=True)
    date = models.DateField(db_index=True)
    # ...

    class Meta:
        indexes = [
            models.Index(fields=['ticker', 'date']),
            models.Index(fields=['date']),
        ]
        ordering = ['-date']
```

## Otimizacao de Queries

### Problema N+1

```python
# RUIM - N+1 queries
inflows = Inflow.objects.all()
for inflow in inflows:
    print(inflow.ticker.name)  # Query para cada ticker
    print(inflow.broker.name)  # Query para cada broker

# BOM - 1 query com JOINs
inflows = Inflow.objects.select_related('ticker', 'broker').all()
for inflow in inflows:
    print(inflow.ticker.name)  # Sem query adicional
    print(inflow.broker.name)  # Sem query adicional
```

### select_related vs prefetch_related

```python
# select_related: ForeignKey e OneToOne (JOIN SQL)
Inflow.objects.select_related('ticker', 'broker')

# prefetch_related: ManyToMany e reverse ForeignKey (query separada)
Ticker.objects.prefetch_related('inflows', 'outflows')
```

### Agregacoes Otimizadas

```python
from django.db.models import Sum, Count, Avg, F

# Agregar em uma unica query
Inflow.objects.aggregate(
    total_invested=Sum('total_price'),
    total_quantity=Sum('quantity'),
    avg_price=Avg('cost_price')
)

# Agregar por grupo
Inflow.objects.values('ticker__category__title').annotate(
    total=Sum('total_price'),
    count=Count('id')
)

# Usar F() para calculos no banco
Inflow.objects.annotate(
    calculated_total=F('quantity') * F('cost_price')
)
```

### Queries Condicionais

```python
from django.db.models import Q, Case, When, Value

# Filtros complexos com Q
Inflow.objects.filter(
    Q(ticker__category__title='FII') | Q(ticker__category__title='Acao'),
    date__year=2024
)

# Case/When para valores condicionais
Dividend.objects.annotate(
    tipo_nome=Case(
        When(income_type='D', then=Value('Dividendo')),
        When(income_type='J', then=Value('JCP')),
        When(income_type='A', then=Value('Amortizacao')),
        default=Value('Outro')
    )
)
```

## Validacoes de Integridade

### Validators nos Models

```python
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class Inflow(models.Model):
    quantity = models.IntegerField(
        validators=[MinValueValidator(1, message='Quantidade deve ser maior que zero')]
    )
    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01, message='Preco deve ser maior que zero')]
    )
    date = models.DateField()

    def clean(self):
        super().clean()
        if self.date and self.date > timezone.now().date():
            raise ValidationError({'date': 'Data nao pode ser futura'})

    def save(self, *args, **kwargs):
        self.full_clean()
        self.total_price = self.quantity * self.cost_price
        super().save(*args, **kwargs)
```

### Constraints no Banco

```python
class Inflow(models.Model):
    # ...

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gt=0),
                name='inflow_quantity_positive'
            ),
            models.CheckConstraint(
                check=models.Q(cost_price__gt=0),
                name='inflow_cost_price_positive'
            ),
            models.UniqueConstraint(
                fields=['ticker', 'date', 'cost_price'],
                name='unique_inflow_per_day_price'
            ),
        ]
```

## Cache com Django-Redis

### Configuracao

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Cache de Queries

```python
from django.core.cache import cache

def get_total_invested():
    cache_key = 'total_invested'
    result = cache.get(cache_key)

    if result is None:
        result = Inflow.objects.aggregate(
            total=Sum('total_price')
        )['total'] or 0
        cache.set(cache_key, result, timeout=300)  # 5 minutos

    return result
```

### Invalidacao de Cache

```python
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

@receiver([post_save, post_delete], sender=Inflow)
def invalidate_inflow_cache(sender, **kwargs):
    cache.delete('total_invested')
    cache.delete('chart_category_data')
```

## Migrations

### Criar Migration

```bash
python manage.py makemigrations
python manage.py makemigrations --name add_indexes_to_inflow inflows
```

### Aplicar Migration

```bash
python manage.py migrate
python manage.py migrate inflows 0005  # Migration especifica
```

### Migration de Dados

```python
# migrations/0006_populate_total_price.py
from django.db import migrations

def calculate_totals(apps, schema_editor):
    Inflow = apps.get_model('inflows', 'Inflow')
    for inflow in Inflow.objects.all():
        inflow.total_price = inflow.quantity * inflow.cost_price
        inflow.save(update_fields=['total_price'])

def reverse_migration(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('inflows', '0005_alter_inflow_type'),
    ]

    operations = [
        migrations.RunPython(calculate_totals, reverse_migration),
    ]
```

## Monitoramento de Queries

### Django Debug Toolbar

```python
# settings/dev.py
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']
```

### Log de Queries

```python
# settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## Checklist de Performance

- [ ] Indices em campos de busca/filtro
- [ ] Indices compostos para queries frequentes
- [ ] select_related em ForeignKeys
- [ ] prefetch_related em relacoes reversas
- [ ] Agregacoes no banco (Sum, Count, Avg)
- [ ] Cache em queries pesadas
- [ ] Paginacao em listas
- [ ] Debug toolbar verificando queries

## Checklist de Integridade

- [ ] Validators em campos numericos
- [ ] Clean() para validacoes complexas
- [ ] Constraints no banco
- [ ] Signals para sincronizacao
- [ ] Testes de validacao
