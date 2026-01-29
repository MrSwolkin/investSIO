# Templates

Documentacao da estrutura de templates do projeto.

## Estrutura de Arquivos

```
app/templates/
├── base.html                    # Template base
├── home.html                    # Dashboard principal
├── negociations.html            # Lista de transacoes
└── components/                  # Componentes reutilizaveis
    ├── _header.html             # Cabecalho
    ├── _sidebar.html            # Menu lateral
    ├── _footer.html             # Rodape
    ├── _category_metrics.html   # Metricas por categoria
    ├── _tickers_metrics.html    # Metricas do ticker
    └── _dividends_table.html    # Tabela de dividendos

brokers/templates/
├── broker_list.html
├── broker_create.html
├── broker_details.html
├── broker_update.html
└── broker_delete.html

tickers/templates/
├── ticker_list.html
├── ticker_create.html
├── ticker_details.html
├── ticker_update.html
└── ticker_delete.html

inflows/templates/
├── inflow_list.html
├── inflow_create.html
├── inflow_details.html
├── inflow_update.html
└── inflow_delete.html

outflows/templates/
├── outflow_list.html
├── outflow_create.html
├── outflow_details.html
├── outflow_update.html
└── outflow_delete.html

dividends/templates/
├── dividend_list.html
├── dividend_create.html
├── dividend_update.html
└── dividend_delete.html
```

---

## Template Base (base.html)

Estrutura principal que todos os templates estendem.

### Blocos Disponiveis

| Bloco | Descricao |
|-------|-----------|
| `{% block title %}` | Titulo da pagina |
| `{% block content %}` | Conteudo principal |

### Bibliotecas Incluidas

- Bootstrap 5.3.3 (CSS e JS via CDN)
- Bootstrap Icons 1.11.3
- Chart.js (para graficos)

### Estrutura

```html
<!DOCTYPE html>
<html lang="pt-BR" data-bs-theme="light">
<head>
    <!-- Bootstrap CSS -->
    <!-- Bootstrap Icons -->
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    {% include "components/_header.html" %}

    <div class="container-fluid">
        <div class="row">
            {% include "components/_sidebar.html" %}

            <main>
                <!-- Mensagens do Django -->
                {% for message in messages %}
                    <div class="alert">{{ message }}</div>
                {% endfor %}

                {% block content %}{% endblock %}
            </main>
        </div>
    </div>

    {% include "components/_footer.html" %}

    <!-- Bootstrap JS -->
</body>
</html>
```

---

## Componentes

### _header.html

Cabecalho simples com titulo centralizado.

### _sidebar.html

Menu lateral com:
- Link para Dashboard
- Link para Corretoras
- Dropdown de Ativos (FII, Acao, Stock, ETF)
- Dropdown de Negociacoes (Todas, Compras, Vendas)
- Link para Dividendos
- Botoes de acao rapida (Nova Compra, Nova Venda)

### _footer.html

Rodape simples.

### _category_metrics.html

Exibe metricas agregadas da categoria:
- Total investido
- Quantidade de ativos
- Preco medio

### _tickers_metrics.html

Exibe metricas do ticker especifico:
- Total investido
- Quantidade atual
- Preco medio

### _dividends_table.html

Tabela de dividendos agrupados por ano e mes.

---

## Padrao de Templates CRUD

### Lista (model_list.html)

```django
{% extends "base.html" %}

{% block content %}
<h1>Lista de Models</h1>

<a href="{% url 'model_create' %}">Novo</a>

<table>
    <thead>
        <tr>
            <th>Campo 1</th>
            <th>Campo 2</th>
            <th>Acoes</th>
        </tr>
    </thead>
    <tbody>
        {% for item in models %}
        <tr>
            <td>{{ item.campo1 }}</td>
            <td>{{ item.campo2 }}</td>
            <td>
                <a href="{% url 'model_details' item.id %}">Ver</a>
                <a href="{% url 'model_update' item.id %}">Editar</a>
                <a href="{% url 'model_delete' item.id %}">Excluir</a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

### Criar/Editar (model_create.html, model_update.html)

```django
{% extends "base.html" %}

{% block content %}
<h1>Criar/Editar Model</h1>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Salvar</button>
</form>
{% endblock %}
```

### Detalhes (model_details.html)

```django
{% extends "base.html" %}

{% block content %}
<h1>Detalhes de {{ model.name }}</h1>

<p>Campo 1: {{ model.campo1 }}</p>
<p>Campo 2: {{ model.campo2 }}</p>

<a href="{% url 'model_update' model.id %}">Editar</a>
<a href="{% url 'model_delete' model.id %}">Excluir</a>
{% endblock %}
```

### Excluir (model_delete.html)

```django
{% extends "base.html" %}

{% block content %}
<h1>Confirmar Exclusao</h1>

<p>Deseja excluir {{ model.name }}?</p>

<form method="post">
    {% csrf_token %}
    <button type="submit">Confirmar</button>
    <a href="{% url 'model_list' %}">Cancelar</a>
</form>
{% endblock %}
```

---

## Variaveis de Contexto

### home.html

| Variavel | Tipo | Descricao |
|----------|------|-----------|
| `total_applied` | dict | Totais por moeda {BRL, USD, EUR} |
| `ipca` | float | Taxa IPCA atual |
| `selic` | float | Taxa SELIC atual |
| `cdi` | float | Taxa CDI atual |
| `inflows_datas` | JSON | Dados para grafico de investimentos |
| `chart_diversity` | JSON | Dados para grafico de diversificacao |
| `chart_total_applied` | JSON | Dados para grafico por moeda |
| `chart_broker` | JSON | Dados para grafico por corretora |
| `last_six_months` | JSON | Labels dos ultimos 6 meses |
| `total_fiis` | JSON | Dividendos de FIIs |
| `total_acoes` | JSON | Dividendos de Acoes |
| `total_stocks` | JSON | Dividendos de Stocks |
| `total_etfs` | JSON | Dividendos de ETFs |

### ticker_details.html

| Variavel | Tipo | Descricao |
|----------|------|-----------|
| `ticker` | Ticker | Objeto do ticker |
| `inflows` | QuerySet | Compras do ticker |
| `outflows` | QuerySet | Vendas do ticker |
| `transactions` | list | Transacoes consolidadas |
| `metrics` | dict | Metricas do ticker |
| `price` | float | Preco atual (API) |
| `ticker_icon` | str | URL do icone (API) |
| `ticker_long_name` | str | Nome completo (API) |
