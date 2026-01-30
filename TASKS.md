### Sprint 1: Seguranca e Configuracao

**Objetivo:** Tornar o sistema seguro e configuravel por ambiente.

**Duracao:** 2 semanas

---

#### EPIC-001: Configuracao de Ambiente

**US-001: Variaveis de Ambiente** `[8 pts]` `[CRITICO]`

> Como desenvolvedor, quero usar variaveis de ambiente para que credenciais nao fiquem expostas no codigo.

**Tarefas:**
- [X] **T-001.1:** Instalar django-environ
  ```bash
  pip install django-environ
  ```
- [X] **T-001.2:** Criar arquivo `.env` na raiz
  ```env
  DEBUG=True
  SECRET_KEY=sua-chave-secreta-aqui
  ALLOWED_HOSTS=localhost,127.0.0.1
  BRAPI_TOKEN=seu-token-aqui
  ```
- [X] **T-001.3:** Criar arquivo `.env.example` (sem valores sensiveis)
- [X] **T-001.4:** Adicionar `.env` ao `.gitignore`
- [X] **T-001.5:** Atualizar `settings.py` para usar `environ.Env()`
- [X] **T-001.6:** Atualizar `services/get_ticker_details.py` para usar env

**Criterios de Aceitacao:**
- [X] Nenhuma credencial no codigo-fonte
- [X] Sistema funciona com `.env`
- [X] `.env` nao esta no git

---

**US-002: Separacao de Settings** `[5 pts]` `[CRITICO]`

> Como desenvolvedor, quero settings separados por ambiente para facilitar deploy.

**Tarefas:**
- [X] **T-002.1:** Criar pasta `app/settings/`
- [X] **T-002.2:** Criar `app/settings/__init__.py`
- [X] **T-002.3:** Criar `app/settings/base.py` (configuracoes comuns)
- [X] **T-002.4:** Criar `app/settings/dev.py` (desenvolvimento)
- [X] **T-002.5:** Criar `app/settings/prod.py` (producao)
- [X] **T-002.6:** Atualizar `manage.py` e `wsgi.py`
- [X] **T-002.7:** Documentar uso em `docs/GETTING_STARTED.md`

**Criterios de Aceitacao:**
- [X] `python manage.py runserver` usa settings.dev
- [X] Settings de prod tem DEBUG=False
- [X] Documentacao atualizada

---

#### EPIC-002: Autenticacao e Autorizacao

**US-003: Protecao de Views** `[8 pts]` `[CRITICO]`

> Como usuario, quero que minhas informacoes sejam protegidas por login.

**Tarefas:**
- [X] **T-003.1:** Adicionar `LoginRequiredMixin` em `brokers/views.py`
- [X] **T-003.2:** Adicionar `LoginRequiredMixin` em `tickers/views.py`
- [X] **T-003.3:** Adicionar `LoginRequiredMixin` em `inflows/views.py`
- [X] **T-003.4:** Adicionar `LoginRequiredMixin` em `outflows/views.py`
- [X] **T-003.5:** Adicionar `LoginRequiredMixin` em `dividends/views.py`
- [X] **T-003.6:** Adicionar `@login_required` em `app/views.py` (home, negociations)
- [X] **T-003.7:** Configurar `LOGIN_URL` em settings
- [X] **T-003.8:** Criar template `registration/login.html`

**Criterios de Aceitacao:**
- [X] Todas as views requerem login
- [X] Usuarios nao autenticados sao redirecionados
- [X] Pagina de login funcional

---

**US-004: Validacao de Input** `[5 pts]` `[ALTO]`

> Como desenvolvedor, quero validar inputs para prevenir ataques.

**Tarefas:**
- [X] **T-004.1:** Validar parametro `ticker` em `dividends/views.py`
- [X] **T-004.2:** Validar parametro `name` em `brokers/views.py`
- [X] **T-004.3:** Validar parametro `category` em `tickers/views.py`
- [X] **T-004.4:** Criar helper `app/utils/validators.py`
- [X] **T-004.5:** Adicionar testes de validacao

**Criterios de Aceitacao:**
- [X] Parametros invalidos retornam 404
- [X] Sem SQL injection possivel
- [X] Testes passando

---

#### EPIC-003: Logging e Monitoramento

**US-005: Configuracao de Logging** `[5 pts]` `[ALTO]`

> Como desenvolvedor, quero logs estruturados para debugar problemas.

**Tarefas:**
- [X] **T-005.1:** Criar pasta `logs/` na raiz
- [X] **T-005.2:** Adicionar `logs/` ao `.gitignore`
- [X] **T-005.3:** Configurar LOGGING em `settings/base.py`
- [X] **T-005.4:** Adicionar logs em `services/get_ticker_details.py`
- [X] **T-005.5:** Adicionar logs em `services/fees_br.py`
- [X] **T-005.6:** Adicionar logs em views criticas

**Criterios de Aceitacao:**
- [X] Logs gravados em arquivo
- [X] Logs de erro em API externa
- [X] Formato consistente

---

**US-006: Tratamento de Erros** `[3 pts]` `[ALTO]`

> Como usuario, quero ver mensagens de erro amigaveis quando algo falha.

**Tarefas:**
- [X] **T-006.1:** Adicionar try/catch em `services/get_ticker_details.py`
- [X] **T-006.2:** Adicionar try/catch em `services/fees_br.py`
- [X] **T-006.3:** Criar template `templates/errors/500.html`
- [X] **T-006.4:** Criar template `templates/errors/404.html`
- [X] **T-006.5:** Configurar handlers em `urls.py`

**Criterios de Aceitacao:**
- [X] APIs falhando nao quebram a pagina
- [X] Mensagens de erro amigaveis
- [X] Erros logados

---

### Sprint 2: Performance e Database

**Objetivo:** Otimizar queries e preparar para escala.

**Duracao:** 2 semanas

---

#### EPIC-004: Otimizacao de Queries

**US-007: Indices em Models** `[5 pts]` `[CRITICO]`

> Como desenvolvedor, quero indices para queries mais rapidas.

**Tarefas:**
- [X] **T-007.1:** Adicionar `db_index=True` em `Inflow.ticker`
- [X] **T-007.2:** Adicionar `db_index=True` em `Inflow.broker`
- [X] **T-007.3:** Adicionar `db_index=True` em `Inflow.date`
- [X] **T-007.4:** Adicionar `db_index=True` em `Outflow.ticker`, `broker`, `date`
- [X] **T-007.5:** Adicionar `db_index=True` em `Dividend.ticker`, `date`
- [X] **T-007.6:** Adicionar `Meta.indexes` compostos
- [X] **T-007.7:** Criar e aplicar migrations

**Criterios de Aceitacao:**
- [X] Migrations criadas sem erro
- [X] Indices aplicados no banco

---

**US-008: Select Related** `[5 pts]` `[CRITICO]`

> Como desenvolvedor, quero eliminar N+1 queries.

**Tarefas:**
- [X] **T-008.1:** Adicionar `select_related()` em `InflowListView`
- [X] **T-008.2:** Adicionar `select_related()` em `OutflowListView`
- [X] **T-008.3:** Adicionar `select_related()` em `DividendListView`
- [X] **T-008.4:** Adicionar `select_related()` em `TickerDetailsView`
- [X] **T-008.5:** Otimizar `app/metrics.py`
- [X] **T-008.6:** Instalar django-debug-toolbar para verificar

**Criterios de Aceitacao:**
- [X] ListViews com no maximo 3 queries
- [X] Debug toolbar mostrando queries otimizadas

---

**US-009: Paginacao** `[3 pts]` `[CRITICO]`

> Como usuario, quero paginacao para carregar dados mais rapido.

**Tarefas:**
- [X] **T-009.1:** Adicionar `paginate_by = 25` em todas as ListViews
- [X] **T-009.2:** Criar componente `_pagination.html`
- [X] **T-009.3:** Adicionar paginacao nos templates de lista
- [X] **T-009.4:** Otimizar `negociations()` view

**Criterios de Aceitacao:**
- [X] Listas paginadas com 25 itens
- [X] Navegacao entre paginas funcional

---

#### EPIC-005: Cache

**US-010: Configuracao de Cache** `[5 pts]` `[ALTO]`

> Como desenvolvedor, quero cache para reduzir carga no banco.

**Tarefas:**
- [X] **T-010.1:** Instalar django-redis e redis
- [X] **T-010.2:** Configurar CACHES em settings
- [X] **T-010.3:** Adicionar cache em `app/metrics.py`
- [X] **T-010.4:** Adicionar `@cache_page` em `home()` view
- [X] **T-010.5:** Documentar invalidacao de cache

**Criterios de Aceitacao:**
- [X] Dashboard carrega em < 500ms (cached)
- [X] Cache invalida ao criar/atualizar dados

---

#### EPIC-006: Validacoes de Models

**US-011: Validators em Models** `[5 pts]` `[ALTO]`

> Como desenvolvedor, quero validacoes para garantir integridade.

**Tarefas:**
- [X] **T-011.1:** Adicionar `MinValueValidator` em `Inflow.quantity`
- [X] **T-011.2:** Adicionar `MinValueValidator` em `Inflow.cost_price`
- [X] **T-011.3:** Adicionar metodo `clean()` em `Inflow`
- [X] **T-011.4:** Repetir para `Outflow` e `Dividend`
- [X] **T-011.5:** Criar testes de validacao

**Criterios de Aceitacao:**
- [X] Nao permite quantidade <= 0
- [X] Nao permite data futura
- [X] Testes passando

---

#### EPIC-007: Testes

**US-012: Setup de Testes** `[3 pts]` `[CRITICO]`

> Como desenvolvedor, quero infraestrutura de testes.

**Tarefas:**
- [X] **T-012.1:** Instalar pytest, pytest-django, pytest-cov
- [X] **T-012.2:** Criar `pytest.ini`
- [X] **T-012.3:** Criar `conftest.py` com fixtures
- [X] **T-012.4:** Criar pasta `tests/` em cada app

**Criterios de Aceitacao:**
- [X] `pytest` executa sem erro
- [X] Estrutura de testes criada

---

**US-013: Testes de Models** `[3 pts]` `[ALTO]`

> Como desenvolvedor, quero testes unitarios de models.

**Tarefas:**
- [X] **T-013.1:** Criar testes para `Broker`
- [X] **T-013.2:** Criar testes para `Ticker`
- [X] **T-013.3:** Criar testes para `Inflow`
- [X] **T-013.4:** Criar testes para `Outflow`
- [X] **T-013.5:** Criar testes para `Dividend`

**Criterios de Aceitacao:**
- [X] Cobertura de models >= 80%
- [X] Testes de validacao incluidos

---

### Sprint 3: Frontend Foundation

**Objetivo:** Configurar TailwindCSS e criar design system.

**Duracao:** 2 semanas

---

#### EPIC-008: Setup TailwindCSS

**US-014: Instalacao Django-Tailwind** `[5 pts]` `[ALTO]`

> Como desenvolvedor, quero TailwindCSS integrado ao Django.

**Tarefas:**
- [X] **T-014.1:** Instalar django-tailwind e django-browser-reload
- [X] **T-014.2:** Executar `python manage.py tailwind init`
- [X] **T-014.3:** Executar `python manage.py tailwind install`
- [X] **T-014.4:** Atualizar `INSTALLED_APPS`
- [X] **T-014.5:** Atualizar `MIDDLEWARE`
- [X] **T-014.6:** Atualizar `urls.py` com browser-reload
- [X] **T-014.7:** Testar `python manage.py tailwind start`

**Criterios de Aceitacao:**
- [X] Tailwind compila sem erros
- [X] Hot reload funcionando

---

**US-015: Configuracao do Design System** `[5 pts]` `[ALTO]`

> Como desenvolvedor, quero um design system consistente.

**Tarefas:**
- [X] **T-015.1:** Configurar `tailwind.config.js` com cores customizadas
- [X] **T-015.2:** Configurar fontes (Inter, Poppins)
- [X] **T-015.3:** Configurar animacoes customizadas
- [X] **T-015.4:** Criar `input.css` com componentes base
- [X] **T-015.5:** Definir classes utilitarias (.btn, .card, .input, etc)

**Criterios de Aceitacao:**
- [X] Design tokens definidos
- [X] Componentes CSS criados
- [X] Dark mode habilitado

---

#### EPIC-009: Layout Principal

**US-016: Template Base** `[5 pts]` `[ALTO]`

> Como usuario, quero uma interface moderna e consistente.

**Tarefas:**
- [X] **T-016.1:** Remover Bootstrap do `base.html`
- [X] **T-016.2:** Adicionar `{% tailwind_css %}`
- [X] **T-016.3:** Criar estrutura responsiva
- [X] **T-016.4:** Implementar sistema de mensagens moderno
- [X] **T-016.5:** Testar em mobile e desktop

**Criterios de Aceitacao:**
- [X] Pagina carrega sem Bootstrap
- [X] Layout responsivo
- [X] Dark mode aplicado

---

**US-017: Header e Sidebar** `[8 pts]` `[ALTO]`

> Como usuario, quero navegacao intuitiva e moderna.

**Tarefas:**
- [X] **T-017.1:** Redesenhar `_header.html`
- [X] **T-017.2:** Adicionar logo e branding
- [X] **T-017.3:** Adicionar busca global
- [X] **T-017.4:** Adicionar menu de usuario
- [X] **T-017.5:** Redesenhar `_sidebar.html`
- [X] **T-017.6:** Implementar dropdowns com Alpine.js
- [X] **T-017.7:** Implementar sidebar colapsavel em mobile
- [X] **T-017.8:** Adicionar botoes de acao rapida

**Criterios de Aceitacao:**
- [X] Header fixo funcional
- [X] Sidebar responsiva
- [X] Dropdowns animados

---

#### EPIC-010: Componentes UI

**US-018: Componentes Base** `[8 pts]` `[MEDIO]`

> Como desenvolvedor, quero componentes reutilizaveis.

**Tarefas:**
- [X] **T-018.1:** Criar `components/ui/_button.html`
- [X] **T-018.2:** Criar `components/ui/_card.html`
- [X] **T-018.3:** Criar `components/ui/_metric_card.html`
- [X] **T-018.4:** Criar `components/ui/_badge.html`
- [X] **T-018.5:** Criar `components/ui/_table.html`
- [X] **T-018.6:** Criar `components/ui/_modal.html`
- [X] **T-018.7:** Criar `components/ui/_alert.html`
- [X] **T-018.8:** Criar `components/ui/_empty_state.html`

**Criterios de Aceitacao:**
- [X] Componentes documentados
- [X] Variantes implementadas
- [X] Usados via `{% include %}`

---

**US-019: Componentes de Form** `[3 pts]` `[MEDIO]`

> Como desenvolvedor, quero formularios estilizados.

**Tarefas:**
- [ ] **T-019.1:** Criar `components/forms/_form_field.html`
- [ ] **T-019.2:** Criar widgets Tailwind em `app/widgets.py`
- [ ] **T-019.3:** Atualizar forms existentes

**Criterios de Aceitacao:**
- [ ] Inputs estilizados
- [ ] Validacao visual
- [ ] Labels e erros exibidos

---

### Sprint 4: CRUD Redesign

**Objetivo:** Redesenhar todas as paginas CRUD.

**Duracao:** 2 semanas

---

#### EPIC-011: Dashboard

**US-020: Redesign Dashboard** `[8 pts]` `[ALTO]`

> Como usuario, quero um dashboard informativo e bonito.

**Tarefas:**
- [ ] **T-020.1:** Redesenhar `home.html` com grid responsivo
- [ ] **T-020.2:** Implementar cards de metricas com gradientes
- [ ] **T-020.3:** Configurar Chart.js para tema escuro
- [ ] **T-020.4:** Redesenhar graficos de diversificacao
- [ ] **T-020.5:** Adicionar loading skeletons
- [ ] **T-020.6:** Otimizar para mobile

**Criterios de Aceitacao:**
- [ ] Metricas exibidas com gradientes
- [ ] Graficos em tema escuro
- [ ] Responsivo em todas as telas

---

#### EPIC-012: Templates CRUD

**US-021: Brokers CRUD** `[5 pts]` `[MEDIO]`

> Como usuario, quero gerenciar corretoras com interface moderna.

**Tarefas:**
- [ ] **T-021.1:** Redesenhar `broker_list.html`
- [ ] **T-021.2:** Redesenhar `broker_create.html`
- [ ] **T-021.3:** Redesenhar `broker_update.html`
- [ ] **T-021.4:** Redesenhar `broker_details.html`
- [ ] **T-021.5:** Implementar modal de delecao

**Criterios de Aceitacao:**
- [ ] Lista com tabela moderna
- [ ] Formularios estilizados
- [ ] Modal de confirmacao

---

**US-022: Tickers CRUD** `[5 pts]` `[MEDIO]`

> Como usuario, quero gerenciar ativos com interface moderna.

**Tarefas:**
- [ ] **T-022.1:** Redesenhar `ticker_list.html`
- [ ] **T-022.2:** Redesenhar `ticker_create.html`
- [ ] **T-022.3:** Redesenhar `ticker_update.html`
- [ ] **T-022.4:** Redesenhar `ticker_details.html`
- [ ] **T-022.5:** Implementar modal de delecao

**Criterios de Aceitacao:**
- [ ] Lista filtrada por categoria
- [ ] Detalhes com metricas visuais
- [ ] Integracao com API de precos

---

**US-023: Inflows CRUD** `[5 pts]` `[MEDIO]`

> Como usuario, quero registrar compras com interface moderna.

**Tarefas:**
- [ ] **T-023.1:** Redesenhar `inflow_list.html`
- [ ] **T-023.2:** Redesenhar `inflow_create.html`
- [ ] **T-023.3:** Redesenhar `inflow_update.html`
- [ ] **T-023.4:** Redesenhar `inflow_details.html`
- [ ] **T-023.5:** Implementar modal de delecao

**Criterios de Aceitacao:**
- [ ] Lista com filtros
- [ ] Formulario com selects modernos
- [ ] Paginacao funcional

---

**US-024: Outflows e Dividends CRUD** `[6 pts]` `[MEDIO]`

> Como usuario, quero gerenciar vendas e dividendos.

**Tarefas:**
- [ ] **T-024.1:** Redesenhar templates de Outflows
- [ ] **T-024.2:** Redesenhar templates de Dividends
- [ ] **T-024.3:** Redesenhar `negociations.html`
- [ ] **T-024.4:** Adicionar filtros avancados
- [ ] **T-024.5:** Implementar export (opcional)

**Criterios de Aceitacao:**
- [ ] Todas as paginas redesenhadas
- [ ] Consistencia visual

---

### Sprint 5: Polish e Deploy

**Objetivo:** Finalizar, testar e preparar deploy.

**Duracao:** 1 semana

---

#### EPIC-013: Quality Assurance

**US-025: Code Cleanup** `[3 pts]` `[MEDIO]`

> Como desenvolvedor, quero codigo limpo e organizado.

**Tarefas:**
- [ ] **T-025.1:** Corrigir typo `OuflowListView` -> `OutflowListView`
- [ ] **T-025.2:** Corrigir typo `dividens` -> `dividends`
- [ ] **T-025.3:** Remover codigo comentado
- [ ] **T-025.4:** Remover app `portifolio/`
- [ ] **T-025.5:** Adicionar docstrings em funcoes principais

**Criterios de Aceitacao:**
- [ ] Zero typos
- [ ] Codigo comentado removido
- [ ] Docstrings em funcoes publicas

---

**US-026: Testes E2E** `[5 pts]` `[ALTO]`

> Como desenvolvedor, quero garantir que tudo funciona.

**Tarefas:**
- [ ] **T-026.1:** Criar testes de views
- [ ] **T-026.2:** Testar fluxo de login
- [ ] **T-026.3:** Testar CRUD de brokers
- [ ] **T-026.4:** Testar CRUD de inflows
- [ ] **T-026.5:** Verificar cobertura >= 70%

**Criterios de Aceitacao:**
- [ ] Testes passando
- [ ] Cobertura >= 70%

---

#### EPIC-014: Acessibilidade e Performance

**US-027: Acessibilidade** `[3 pts]` `[MEDIO]`

> Como usuario com deficiencia, quero usar o sistema.

**Tarefas:**
- [ ] **T-027.1:** Adicionar atributos ARIA
- [ ] **T-027.2:** Verificar contraste de cores (WCAG AA)
- [ ] **T-027.3:** Testar navegacao por teclado
- [ ] **T-027.4:** Adicionar `alt` em imagens

**Criterios de Aceitacao:**
- [ ] Score Lighthouse >= 90
- [ ] Navegacao por teclado funcional

---

**US-028: Performance Final** `[3 pts]` `[MEDIO]`

> Como usuario, quero paginas rapidas.

**Tarefas:**
- [ ] **T-028.1:** Purge CSS nao utilizado
- [ ] **T-028.2:** Minificar assets
- [ ] **T-028.3:** Verificar Lighthouse Performance
- [ ] **T-028.4:** Otimizar imagens

**Criterios de Aceitacao:**
- [ ] CSS < 30KB gzipped
- [ ] FCP < 1.5s
- [ ] LCP < 2.5s

---

#### EPIC-015: Documentacao

**US-029: Atualizacao de Docs** `[4 pts]` `[BAIXO]`

> Como desenvolvedor, quero documentacao atualizada.

**Tarefas:**
- [ ] **T-029.1:** Atualizar `docs/GETTING_STARTED.md`
- [ ] **T-029.2:** Atualizar `docs/ARCHITECTURE.md`
- [ ] **T-029.3:** Documentar design system
- [ ] **T-029.4:** Criar `CHANGELOG.md`

**Criterios de Aceitacao:**
- [ ] Docs refletem estado atual
- [ ] Changelog completo

---

## 6. Especificacoes Tecnicas

### 6.1 Design System

#### Paleta de Cores (Dark Theme)

| Token | Hex | Tailwind | Uso |
|-------|-----|----------|-----|
| `bg-base` | `#0f172a` | `slate-900` | Background principal |
| `bg-surface` | `#1e293b` | `slate-800` | Cards, modais |
| `bg-elevated` | `#334155` | `slate-700` | Hover states |
| `text-primary` | `#f1f5f9` | `slate-100` | Titulos |
| `text-secondary` | `#cbd5e1` | `slate-300` | Labels |

#### Gradientes

| Nome | Classes | Uso |
|------|---------|-----|
| Primary | `from-blue-500 to-cyan-500` | CTAs |
| Success | `from-emerald-500 to-teal-500` | Compras |
| Danger | `from-red-500 to-pink-500` | Vendas |

### 6.2 Componentes CSS

Ver arquivo `input.css` para implementacao completa.

### 6.3 Estrutura de Settings

```
app/settings/
├── __init__.py
├── base.py      # Configuracoes comuns
├── dev.py       # DEBUG=True, SQLite
└── prod.py      # DEBUG=False, PostgreSQL
```

---

## 7. Definition of Done (DoD)

Uma tarefa so e considerada **DONE** quando:

### Codigo
- [ ] Codigo escrito e funcionando
- [ ] Sem erros de lint
- [ ] Sem warnings no console
- [ ] Code review aprovado (se aplicavel)

### Testes
- [ ] Testes unitarios passando
- [ ] Cobertura >= 70% (novas funcionalidades)
- [ ] Testes manuais realizados

### Documentacao
- [ ] Docstrings adicionadas
- [ ] Docs atualizados (se necessario)

### UX
- [ ] Responsivo (mobile, tablet, desktop)
- [ ] Acessivel (navegacao por teclado)
- [ ] Feedback visual (loading, success, error)

---

## 8. Metricas de Sucesso

### 8.1 Performance

| Metrica | Meta | Ferramenta |
|---------|------|------------|
| First Contentful Paint | < 1.5s | Lighthouse |
| Largest Contentful Paint | < 2.5s | Lighthouse |
| Time to Interactive | < 3s | Lighthouse |
| Cumulative Layout Shift | < 0.1 | Lighthouse |
| Database Queries/Page | < 10 | Debug Toolbar |

### 8.2 Qualidade

| Metrica | Meta | Ferramenta |
|---------|------|------------|
| Test Coverage | >= 70% | pytest-cov |
| Lighthouse Performance | >= 90 | Lighthouse |
| Lighthouse Accessibility | >= 90 | Lighthouse |
| Security Vulnerabilities | 0 | Django check |

### 8.3 UX

| Metrica | Meta | Metodo |
|---------|------|--------|
| Mobile Usability | >= 90 | Lighthouse |
| Contraste WCAG AA | 100% | Lighthouse |
| Tempo para tarefa | -30% | Teste usuario |

---

## 9. Dependencias

### 9.1 requirements.txt (Atualizado)

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

# Debug (dev only)
django-debug-toolbar==4.2.0

# Testes
pytest==7.4.3
pytest-django==4.7.0
pytest-cov==4.1.0

# Database (producao)
psycopg2-binary==2.9.9

# API REST (futuro)
djangorestframework==3.14.0
```

### 9.2 CDNs

```html
<!-- Bootstrap Icons -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<!-- Alpine.js -->
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>

<!-- Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@600;700;800&display=swap" rel="stylesheet">
```

---

## 10. Referencias

### Documentacao Oficial
- [Django Documentation](https://docs.djangoproject.com/)
- [Django-Tailwind](https://django-tailwind.readthedocs.io/)
- [TailwindCSS](https://tailwindcss.com/docs)
- [Alpine.js](https://alpinejs.dev/)

### Best Practices
- [Django Security](https://docs.djangoproject.com/en/5.0/topics/security/)
- [Django Performance](https://docs.djangoproject.com/en/5.0/topics/performance/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)

### Documentacao do Projeto
- [Getting Started](./docs/GETTING_STARTED.md)
- [Architecture](./docs/ARCHITECTURE.md)
- [Models](./docs/MODELS.md)
- [Backend Improvements](./docs/BACKEND_IMPROVEMENTS.md)

---