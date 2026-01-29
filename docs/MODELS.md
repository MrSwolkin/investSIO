# Models

Documentacao dos models do projeto InvestSIO.

## Diagrama de Relacionamentos

```
┌─────────────┐     ┌─────────────┐
│  Currency   │     │  Category   │
└──────┬──────┘     └──────┬──────┘
       │                   │
       ├───────┐    ┌──────┘
       │       │    │
       ▼       ▼    ▼
┌─────────┐  ┌─────────┐
│ Broker  │  │ Ticker  │
└────┬────┘  └────┬────┘
     │            │
     │     ┌──────┼──────┐
     │     │      │      │
     ▼     ▼      ▼      ▼
┌─────────┐ ┌─────────┐ ┌──────────┐
│ Inflow  │ │ Outflow │ │ Dividend │
└─────────┘ └─────────┘ └──────────┘
```

---

## brokers.Currency

Representa as moedas suportadas pelo sistema.

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `code` | CharField(5) | Codigo da moeda (BRL, USD, EUR) |
| `name` | CharField(50) | Nome da moeda |
| `exchange_rate` | DecimalField(10,4) | Taxa de cambio (opcional) |

**Relacionamentos:**
- `brokers` → Broker (reverse)
- `tickers` → Ticker (reverse)

---

## brokers.Broker

Representa uma corretora de investimentos.

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `name` | CharField(100) | Nome da corretora |
| `account_number` | CharField(500) | Numero da conta (opcional) |
| `country` | CharField(20) | Pais (opcional) |
| `currency` | ForeignKey(Currency) | Moeda principal |
| `description` | TextField | Descricao (opcional) |

**Relacionamentos:**
- `currency` → Currency
- `inflows` → Inflow (reverse)
- `outflows` → Outflow (reverse)

---

## categories.Category

Representa uma categoria de ativo.

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `title` | CharField(20) | Titulo (FII, Acao, Stock, ETF) |
| `description` | TextField | Descricao (opcional) |

**Relacionamentos:**
- `tickers` → Ticker (reverse)

---

## tickers.Ticker

Representa um ativo financeiro.

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `name` | CharField(10) | Codigo do ticker (MGLU3, BBAS3) |
| `category` | ForeignKey(Category) | Categoria do ativo |
| `quantity` | IntegerField | Quantidade (legado, nao usado) |
| `currency` | ForeignKey(Currency) | Moeda do ativo |
| `sector` | CharField(100) | Setor economico (opcional) |
| `description` | TextField(500) | Descricao (opcional) |

**Relacionamentos:**
- `category` → Category
- `currency` → Currency
- `inflows` → Inflow (reverse)
- `outflows` → Outflow (reverse)
- `dividens` → Dividend (reverse)

**Propriedades:**
- `total_quantity` → Calcula quantidade atual via metrics

---

## inflows.Inflow

Representa uma compra de ativo.

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `broker` | ForeignKey(Broker) | Corretora (opcional) |
| `ticker` | ForeignKey(Ticker) | Ativo comprado |
| `cost_price` | DecimalField(10,2) | Preco unitario |
| `quantity` | IntegerField | Quantidade |
| `total_price` | DecimalField(10,2) | Total (auto-calculado) |
| `date` | DateField | Data da compra |
| `tax` | DecimalField(10,2) | Taxas/custos |
| `type` | CharField | Tipo: "Compra" ou "Subscricao" |

**Relacionamentos:**
- `broker` → Broker
- `ticker` → Ticker

**Auto-calculo no save():**
```python
total_price = cost_price * quantity
```

---

## outflows.Outflow

Representa uma venda de ativo.

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `broker` | ForeignKey(Broker) | Corretora (opcional) |
| `ticker` | ForeignKey(Ticker) | Ativo vendido |
| `cost_price` | DecimalField(10,2) | Preco unitario |
| `quantity` | IntegerField | Quantidade |
| `total_price` | DecimalField(10,2) | Total (auto-calculado) |
| `date` | DateField | Data da venda |
| `tax` | DecimalField(10,2) | Taxas/custos |

**Relacionamentos:**
- `broker` → Broker
- `ticker` → Ticker

**Auto-calculo no save():**
```python
total_price = cost_price * quantity
```

---

## dividends.Dividend

Representa um dividendo recebido.

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `ticker` | ForeignKey(Ticker) | Ativo que gerou o dividendo |
| `value` | DecimalField(12,10) | Valor por cota |
| `date` | DateField | Data de pagamento |
| `currency` | CharField | Moeda: "BRL" ou "USD" |
| `quantity_quote` | IntegerField | Quantidade de cotas (auto-calculado) |
| `total_value` | DecimalField(10,2) | Total recebido (auto-calculado) |
| `income_type` | CharField | Tipo: "D", "J" ou "A" |

**Tipos de rendimento:**
- `D` = Dividendos
- `J` = Juros sobre Capital Proprio (JCP)
- `A` = Amortizacao

**Relacionamentos:**
- `ticker` → Ticker

**Auto-calculo no save():**
```python
# Calcula quantidade de cotas na data do dividendo
quantity_quote = sum(inflows até a data) - sum(outflows até a data)
total_value = value * quantity_quote
```

---

## dividends.DeclaredDividend

Representa um dividendo declarado (futuro).

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `ticker` | ForeignKey(Ticker) | Ativo |
| `value_per_share` | DecimalField(10,2) | Valor por cota declarado |
| `payment_date` | DateField | Data de pagamento prevista |

**Relacionamentos:**
- `ticker` → Ticker
