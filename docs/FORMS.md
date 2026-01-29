# Forms

Documentacao dos formularios do projeto.

## Visao Geral

Todos os forms herdam de `forms.ModelForm` e usam widgets com classes Bootstrap.

---

## BrokerForm (brokers/forms.py)

Formulario para criar/editar corretoras.

| Campo | Widget | Classes |
|-------|--------|---------|
| `name` | TextInput | `form-control mt-2` |
| `account_number` | TextInput | `form-control mt-2` |
| `country` | TextInput | `form-control mt-2` |
| `currency` | Select | `form-control mt-2 form-select` |
| `description` | Textarea | `form-control mt-2` (3 linhas) |

**Labels:**
- Nome da corretora
- N da conta
- Pais
- Moeda
- Descricao

---

## TickerForms (tickers/forms.py)

Formulario para criar/editar tickers.

| Campo | Widget | Classes |
|-------|--------|---------|
| `name` | TextInput | `form-control mt-2` |
| `category` | Select | `form-control mt-2 form-select` |
| `currency` | Select | `form-control mt-2 form-select` |
| `sector` | TextInput | `form-control mt-2` |
| `description` | Textarea | `form-control mt-2` |

**Labels:**
- Codigo do Ticker
- Categoria
- Moeda
- Setor
- Descricao

---

## InflowForms (inflows/forms.py)

Formulario para registrar compras.

| Campo | Widget | Classes |
|-------|--------|---------|
| `ticker` | Select | `form-control mt-2 form-select` |
| `date` | DateInput | `form-control mt-2` (placeholder: DD/MM/AAAA) |
| `type` | Select | `form-control mt-2 form-select` |
| `broker` | Select | `form-control mt-2 form-select` |
| `cost_price` | NumberInput | `form-control mt-2` |
| `quantity` | NumberInput | `form-control mt-2` |
| `tax` | NumberInput | `form-control mt-2` |

**Labels:**
- Ticker
- Data
- Compra ou Subscricao
- Corretora
- Preco por cota
- Quantidade
- Taxas

**Choices para tipo:**
- Compra
- Subscricao

---

## OutflowForms (outflows/forms.py)

Formulario para registrar vendas.

| Campo | Widget | Classes |
|-------|--------|---------|
| `ticker` | Select | `form-control mt-2 form-select` |
| `broker` | Select | `form-control mt-2 form-select` |
| `cost_price` | NumberInput | `form-control mt-2` |
| `quantity` | NumberInput | `form-control mt-2` |
| `date` | DateInput | `form-control mt-2` |
| `tax` | NumberInput | `form-control mt-2` |

**Labels:**
- Ticker
- Corretora
- Preco por cota
- Quantidade
- Data
- Taxas

---

## DividendForm (dividends/forms.py)

Formulario para registrar dividendos.

| Campo | Widget | Classes |
|-------|--------|---------|
| `ticker` | Select | `form-control mt-2 form-select` |
| `value` | NumberInput | `form-control mt-2` |
| `date` | DateInput | `form-control mt-2` |
| `income_type` | Select | `form-control mt-2 form-select` |
| `currency` | Select | `form-control mt-2 form-select` |

**Labels:**
- nome do Ticker
- Valor pago por conta
- Data
- Tipo de rendimento
- Moeda

**Choices para income_type:**
- D = Dividendos
- J = Juros de Capital Proprio
- A = Amortizacao

**Choices para currency:**
- BRL = Real
- USD = Dolar

**Nota:** O campo `quantity_quote` e calculado automaticamente no model.

---

## Padrao de Widget

```python
from django import forms

class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ['campo1', 'campo2', 'campo3']
        widgets = {
            'campo1': forms.TextInput(attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Digite aqui'
            }),
            'campo2': forms.Select(attrs={
                'class': 'form-control mt-2 form-select'
            }),
            'campo3': forms.NumberInput(attrs={
                'class': 'form-control mt-2'
            }),
        }
        labels = {
            'campo1': 'Label do Campo 1',
            'campo2': 'Label do Campo 2',
            'campo3': 'Label do Campo 3',
        }
```

---

## Renderizacao nos Templates

Os forms sao renderizados usando `{{ form.as_p }}`:

```django
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary">Salvar</button>
</form>
```

Ou campo por campo para maior controle:

```django
<form method="post">
    {% csrf_token %}

    <div class="mb-3">
        <label for="{{ form.name.id_for_label }}">Nome</label>
        {{ form.name }}
        {% if form.name.errors %}
            <div class="text-danger">{{ form.name.errors }}</div>
        {% endif %}
    </div>

    <button type="submit" class="btn btn-primary">Salvar</button>
</form>
```
