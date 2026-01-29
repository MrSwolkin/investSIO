# Documentacao InvestSIO

Documentacao tecnica do projeto InvestSIO - Sistema de Gerenciamento de Investimentos.

## Indice

| Documento | Descricao |
|-----------|-----------|
| [Getting Started](./GETTING_STARTED.md) | Como configurar e rodar o projeto |
| [Arquitetura](./ARCHITECTURE.md) | Estrutura de pastas e organizacao do projeto |
| [Models](./MODELS.md) | Documentacao dos models e banco de dados |
| [URLs e Views](./URLS.md) | Endpoints e views disponiveis |
| [Templates](./TEMPLATES.md) | Estrutura de templates Django |
| [Forms](./FORMS.md) | Formularios e widgets |
| [Services](./SERVICES.md) | Integracao com APIs externas |
| [Backend Improvements](./BACKEND_IMPROVEMENTS.md) | Melhorias de backend recomendadas |

## Visao Geral

O InvestSIO e uma aplicacao Django para gerenciamento de investimentos pessoais, permitindo:

- Cadastro de corretoras
- Cadastro de ativos (Acoes, FIIs, Stocks, ETFs)
- Registro de compras e vendas
- Registro de dividendos e rendimentos
- Dashboard com metricas e graficos

## Stack Tecnologica

| Tecnologia | Versao |
|------------|--------|
| Python | 3.13 |
| Django | 6.0.1 |
| SQLite | 3 |
| Bootstrap | 5.3.3 |
| Chart.js | Latest |

## Estrutura de Apps

```
investSIO/
├── app/          # Projeto principal (settings, urls, views)
├── brokers/      # Gerenciamento de corretoras
├── tickers/      # Gerenciamento de ativos
├── inflows/      # Registro de compras
├── outflows/     # Registro de vendas
├── dividends/    # Registro de dividendos
├── categories/   # Categorias de ativos
├── portifolio/   # Portfolio (reservado)
└── services/     # Integracao com APIs
```

## Links Uteis

- [PRD do Projeto](../PRD.md) - Documento de requisitos e melhorias planejadas
