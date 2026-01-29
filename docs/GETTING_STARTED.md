# Getting Started

Guia para configurar e rodar o projeto InvestSIO.

## Pre-requisitos

- Python 3.13+
- pip
- Git

## Instalacao

### 1. Clonar o repositorio

```bash
git clone <url-do-repositorio>
cd investSIO
```

### 2. Criar e ativar ambiente virtual

```bash
# Criar venv (se ainda nao existir)
python3 -m venv venv

# Ativar venv
source venv/bin/activate  # Linux/macOS
# ou
.\venv\Scripts\activate   # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar migracoes

```bash
python3 manage.py migrate
```

### 5. Criar superusuario (opcional)

```bash
python3 manage.py createsuperuser
```

### 6. Rodar o servidor

```bash
python3 manage.py runserver
```

O sistema estara disponivel em: `http://localhost:8000`

## URLs Principais

| URL | Descricao |
|-----|-----------|
| `/` | Dashboard principal |
| `/admin/` | Admin Django |
| `/brokers/list/` | Lista de corretoras |
| `/tickers/<categoria>/` | Lista de ativos por categoria |
| `/inflows/list/` | Lista de compras |
| `/outflow/list/` | Lista de vendas |
| `/dividends/list/` | Lista de dividendos |
| `/negociations/` | Todas as transacoes |

## Dependencias

```txt
Django==6.0.1
requests==2.32.5
python-dateutil==2.9.0.post0
```

## Banco de Dados

O projeto usa SQLite por padrao. O arquivo do banco e `db.sqlite3` na raiz do projeto.

## Ambiente de Desenvolvimento

O projeto esta configurado com `DEBUG=True`. Para producao, altere em `app/settings.py`.
