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

### 4. Configurar variaveis de ambiente

Copie o arquivo `.env.example` para `.env` e configure as variaveis:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configuracoes:

```env
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
ALLOWED_HOSTS=localhost,127.0.0.1
BRAPI_TOKEN=seu-token-brapi-aqui
```

### 5. Aplicar migracoes

```bash
python3 manage.py migrate
```

### 6. Criar superusuario (opcional)

```bash
python3 manage.py createsuperuser
```

### 7. Rodar o servidor

```bash
python3 manage.py runserver
```

O sistema estara disponivel em: `http://localhost:8000`

## Estrutura de Settings

O projeto usa settings separados por ambiente:

```
app/settings/
├── __init__.py
├── base.py      # Configuracoes comuns
├── dev.py       # Desenvolvimento (DEBUG=True, SQLite)
└── prod.py      # Producao (DEBUG=False, PostgreSQL)
```

### Desenvolvimento (padrao)

Por padrao, `manage.py` usa `app.settings.dev`:

```bash
python3 manage.py runserver
```

### Producao

Para usar settings de producao, defina a variavel de ambiente:

```bash
export DJANGO_SETTINGS_MODULE=app.settings.prod
python3 manage.py runserver
```

Ou especifique diretamente:

```bash
python3 manage.py runserver --settings=app.settings.prod
```

### Variaveis de ambiente para producao

Adicione ao `.env` para producao:

```env
DEBUG=False
SECRET_KEY=chave-segura-para-producao
ALLOWED_HOSTS=seudominio.com,www.seudominio.com

# PostgreSQL
DB_NAME=investsio
DB_USER=postgres
DB_PASSWORD=senha-segura
DB_HOST=localhost
DB_PORT=5432

# HTTPS
SECURE_SSL_REDIRECT=True
```

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
django-environ==0.11.2
```

## Banco de Dados

- **Desenvolvimento:** SQLite (`db.sqlite3` na raiz)
- **Producao:** PostgreSQL (configurar via `.env`)
