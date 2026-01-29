# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

InvestSIO is a Django application for personal investment management. It tracks brokers, tickers (stocks, FIIs, ETFs), purchases (inflows), sales (outflows), and dividends.

**Stack:** Python 3.13, Django 6.0.1, SQLite, Bootstrap 5.3.3, Chart.js

## Development Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run development server
python3 manage.py runserver

# Apply migrations
python3 manage.py migrate

# Create new migrations after model changes
python3 manage.py makemigrations

# Create superuser for admin access
python3 manage.py createsuperuser

# Import FII tickers (custom management command)
python3 manage.py import_fiis
```

## Architecture

### Django Apps

| App | Purpose |
|-----|---------|
| `app/` | Main project: settings, root URLs, dashboard views, metrics calculations |
| `brokers/` | Broker and Currency CRUD |
| `tickers/` | Asset (Ticker) CRUD |
| `inflows/` | Purchase transactions CRUD |
| `outflows/` | Sale transactions CRUD |
| `dividends/` | Dividend records CRUD |
| `categories/` | Asset categories (managed via Django Admin) |
| `services/` | External API integrations |

### Key Files

- `app/metrics.py` - Portfolio calculation functions (totals, averages, charts data)
- `app/views.py` - Dashboard (`home`) and transactions list (`negociations`) views
- `services/get_ticker_details.py` - BrAPI integration for real-time ticker data
- `services/fees_br.py` - BrasilAPI integration for economic rates (SELIC, CDI, IPCA)

### Model Relationships

```
Currency ──► Broker ──► Inflow/Outflow
    │
    └──► Ticker ──► Inflow/Outflow/Dividend
           │
Category ──┘
```

- `Inflow` and `Outflow` auto-calculate `total_price` on save
- `Dividend` auto-calculates `quantity_quote` based on holdings at payment date

### View Patterns

All CRUD apps use Django Class-Based Views:
- `<Model>ListView`, `<Model>CreateView`, `<Model>DetailsView`, `<Model>UpdateView`, `<Model>DeleteView`

### URL Patterns

- `/<app>/list/` - List view
- `/<app>/create/` - Create form
- `/<app>/<id>/details/` - Detail view
- `/<app>/<id>/update/` - Update form
- `/<app>/<id>/delete/` - Delete confirmation

## External APIs

- **BrAPI** (`brapi.dev`) - Brazilian stock market data (requires token)
- **BrasilAPI** (`brasilapi.com.br`) - Economic indicators (SELIC, CDI, IPCA)

## Language

The codebase uses Portuguese for:
- Model field names and docstrings
- Template content
- User-facing messages

Code structure and Django patterns follow English conventions.
