# Changelog

Todas as mudancas notaveis deste projeto serao documentadas neste arquivo.

O formato e baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semantico](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Adicionado
- Documentacao do Design System (`docs/DESIGN_SYSTEM.md`)
- Changelog do projeto (`CHANGELOG.md`)

---

## [1.0.0] - 2025-01-31

### Sprint 5: Polish e Deploy

#### Adicionado
- **US-025:** Code Cleanup
  - Correcao de typos (`OuflowListView` -> `OutflowListView`, `dividens` -> `dividends`)
  - Remocao de codigo comentado
  - Remocao do app `portifolio/` nao utilizado
  - Docstrings em funcoes principais

- **US-026:** Testes E2E
  - Testes de views (`app/tests/test_views.py`)
  - Testes de autenticacao (`app/tests/test_auth.py`)
  - Testes CRUD para Brokers, Tickers, Inflows, Outflows, Dividends
  - Cobertura de testes >= 87%
  - Settings de teste (`app/settings/test.py`)

- **US-027:** Acessibilidade
  - Atributos ARIA em todos os componentes
  - Skip navigation link
  - Contraste de cores WCAG AA
  - Suporte a navegacao por teclado
  - `alt` em imagens

- **US-028:** Performance
  - CSS purge automatico via TailwindCSS v4
  - CSS gzipped < 10KB
  - Assets minificados em producao

- **US-029:** Documentacao
  - Atualizacao de `docs/GETTING_STARTED.md`
  - Atualizacao de `docs/ARCHITECTURE.md`
  - Documentacao do Design System

---

## [0.4.0] - 2025-01-30

### Sprint 4: CRUD Redesign

#### Adicionado
- **US-020:** Redesign Dashboard
  - Grid responsivo de metricas
  - Cards de metricas com gradientes
  - Graficos Chart.js em tema escuro
  - Loading skeletons
  - Otimizacao mobile

- **US-021:** Brokers CRUD
  - Lista moderna com tabela estilizada
  - Formularios com TailwindCSS
  - Modal de confirmacao de delecao

- **US-022:** Tickers CRUD
  - Lista filtrada por categoria
  - Detalhes com metricas visuais
  - Integracao com API de precos

- **US-023:** Inflows CRUD
  - Lista com filtros avancados
  - Formularios com selects modernos
  - Paginacao funcional

- **US-024:** Outflows e Dividends CRUD
  - Templates redesenhados
  - Pagina de negociacoes atualizada
  - Consistencia visual em todo CRUD

---

## [0.3.0] - 2025-01-30

### Sprint 3: Frontend Foundation

#### Adicionado
- **US-014:** Instalacao Django-Tailwind
  - django-tailwind integrado
  - django-browser-reload para hot reload
  - Compilacao automatica

- **US-015:** Design System
  - Cores customizadas (dark theme)
  - Fontes Inter e Poppins
  - Animacoes customizadas
  - Componentes CSS base

- **US-016:** Template Base
  - Remocao do Bootstrap
  - Estrutura responsiva com TailwindCSS
  - Sistema de mensagens moderno
  - Dark mode como padrao

- **US-017:** Header e Sidebar
  - Header fixo com busca global
  - Menu de usuario com dropdown
  - Sidebar responsiva com Alpine.js
  - Navegacao mobile

- **US-018:** Componentes UI
  - Button (`_button.html`)
  - Card (`_card.html`)
  - Metric Card (`_metric_card.html`)
  - Badge (`_badge.html`)
  - Table (`_table.html`)
  - Modal (`_modal.html`)
  - Alert (`_alert.html`)
  - Empty State (`_empty_state.html`)

- **US-019:** Componentes de Form
  - Form Field (`_form_field.html`)
  - Widgets Tailwind (`app/widgets.py`)

---

## [0.2.0] - 2025-01-29

### Sprint 2: Performance e Database

#### Adicionado
- **US-007:** Indices em Models
  - `db_index=True` em campos frequentes
  - Indices compostos para queries otimizadas

- **US-008:** Select Related
  - `select_related()` em ListViews
  - Eliminacao de N+1 queries
  - django-debug-toolbar para monitoramento

- **US-009:** Paginacao
  - `paginate_by = 25` em ListViews
  - Componente de paginacao

- **US-010:** Cache
  - django-redis integrado
  - Cache em metricas do dashboard
  - Invalidacao automatica

- **US-011:** Validators em Models
  - `MinValueValidator` em quantidades e precos
  - Metodo `clean()` para validacoes customizadas
  - Testes de validacao

- **US-012:** Setup de Testes
  - pytest e pytest-django
  - pytest-cov para cobertura
  - Fixtures em `conftest.py`

- **US-013:** Testes de Models
  - Testes para todos os models
  - Cobertura >= 80%

---

## [0.1.0] - 2025-01-28

### Sprint 1: Seguranca e Configuracao

#### Adicionado
- **US-001:** Variaveis de Ambiente
  - django-environ integrado
  - Arquivo `.env` para configuracoes
  - Credenciais removidas do codigo

- **US-002:** Separacao de Settings
  - `app/settings/base.py` - configuracoes comuns
  - `app/settings/dev.py` - desenvolvimento
  - `app/settings/prod.py` - producao

- **US-003:** Protecao de Views
  - `LoginRequiredMixin` em todas as views
  - `@login_required` em function views
  - Template de login

- **US-004:** Validacao de Input
  - Validadores em `app/utils/validators.py`
  - Protecao contra SQL injection

- **US-005:** Logging
  - Configuracao LOGGING em settings
  - Logs estruturados em arquivo
  - Logs de erro em APIs externas

- **US-006:** Tratamento de Erros
  - try/catch em servicos externos
  - Templates de erro 404 e 500
  - Mensagens de erro amigaveis

---

## [0.0.1] - 2025-01-25

### Versao Inicial

#### Adicionado
- Estrutura basica do projeto Django
- Models: Broker, Currency, Category, Ticker, Inflow, Outflow, Dividend
- Views CRUD para todos os models
- Templates basicos com Bootstrap
- Integracao com BrAPI para cotacoes
- Integracao com BrasilAPI para taxas economicas
- Dashboard com metricas e graficos
- Admin Django configurado
