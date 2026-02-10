# Getting Started

Guia para configurar e rodar o projeto InvestSIO.

## Pre-requisitos

- Python 3.13+
- Node.js 18+ (para TailwindCSS)
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

### 3. Instalar dependencias Python

```bash
pip install -r requirements.txt
```

### 4. Instalar dependencias Node.js (TailwindCSS)

```bash
python3 manage.py tailwind install
```

### 5. Configurar variaveis de ambiente

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

### 6. Aplicar migracoes

```bash
python3 manage.py migrate
```

### 7. Criar superusuario (opcional)

```bash
python3 manage.py createsuperuser
```

### 8. Rodar o servidor de desenvolvimento

Em dois terminais separados:

**Terminal 1 - TailwindCSS:**
```bash
python3 manage.py tailwind start
```

**Terminal 2 - Django:**
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
├── prod.py      # Producao (DEBUG=False, PostgreSQL)
└── test.py      # Testes (banco em memoria)
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

# Redis (para cache)
REDIS_URL=redis://localhost:6379/1

# HTTPS
SECURE_SSL_REDIRECT=True
```

## URLs Principais

| URL | Descricao |
|-----|-----------|
| `/` | Dashboard principal |
| `/admin/` | Admin Django |
| `/login/` | Pagina de login |
| `/brokers/list/` | Lista de corretoras |
| `/tickers/<categoria>/` | Lista de ativos por categoria |
| `/inflows/list/` | Lista de compras |
| `/outflow/list/` | Lista de vendas |
| `/dividends/list/` | Lista de dividendos |
| `/negociations/` | Todas as transacoes |

## Executar Testes

```bash
# Rodar todos os testes
pytest

# Com cobertura de codigo
pytest --cov=. --cov-report=html

# Arquivo de cobertura gerado em htmlcov/index.html
```

## Build para Producao

```bash
# Compilar CSS para producao (minificado)
python3 manage.py tailwind build

# Coletar arquivos estaticos
python3 manage.py collectstatic
```

## Dependencias Principais

```txt
# Core
Django==6.0.1
requests==2.32.5
python-dateutil==2.9.0.post0

# Configuracao
django-environ==0.11.2

# Frontend
django-tailwind[reload]==4.0.0
django-browser-reload==1.12.1

# Performance
django-redis==5.4.0
redis==5.0.1

# Testes
pytest==7.4.3
pytest-django==4.7.0
pytest-cov==4.1.0
```

## Banco de Dados

- **Desenvolvimento:** SQLite (`db.sqlite3` na raiz)
- **Testes:** SQLite em memoria (`:memory:`)
- **Producao:** PostgreSQL (configurar via `.env`)
