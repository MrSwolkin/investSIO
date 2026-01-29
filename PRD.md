# PRD - Product Requirements Document
## InvestSIO - Modernizacao Completa (Frontend + Backend)

**Versao:** 3.0
**Data:** 29/01/2026
**Status:** Aprovado
**Framework:** Django 6.0.1 + django-tailwind 4.0.0

---

## Sumario Executivo

O **InvestSIO** e uma aplicacao Django para gerenciamento de investimentos pessoais. Este documento detalha a modernizacao completa do sistema, abrangendo:

- **Backend:** Seguranca, performance, qualidade de codigo e escalabilidade
- **Frontend:** Migracao para TailwindCSS com design system moderno e responsivo

---

## Indice

1. [Estado Atual](#1-estado-atual)
2. [Problemas Identificados](#2-problemas-identificados)
3. [Visao do Produto](#3-visao-do-produto)
4. [Epicos e Sprints](#4-epicos-e-sprints)
5. [Sprint Backlog Detalhado](#5-sprint-backlog-detalhado)
6. [Especificacoes Tecnicas](#6-especificacoes-tecnicas)
7. [Definition of Done (DoD)](#7-definition-of-done-dod)
8. [Metricas de Sucesso](#8-metricas-de-sucesso)
9. [Dependencias](#9-dependencias)
10. [Referencias](#10-referencias)

---

## 1. Estado Atual

### 1.1 Stack Tecnologica

| Camada | Tecnologia | Versao | Status |
|--------|------------|--------|--------|
| Backend | Django | 6.0.1 | Atual |
| Backend | Python | 3.13 | Atual |
| Database | SQLite | 3 | A migrar |
| Frontend | Bootstrap | 5.3.3 | A remover |
| Frontend | TailwindCSS | - | A implementar |
| Icons | Bootstrap Icons | 1.11.3 | Manter |
| Charts | Chart.js | Latest | Manter |

### 1.2 Arquitetura Atual

```
investSIO/
├── app/                 # Projeto principal
├── brokers/             # CRUD corretoras
├── tickers/             # CRUD ativos
├── inflows/             # CRUD compras
├── outflows/            # CRUD vendas
├── dividends/           # CRUD dividendos
├── categories/          # Categorias
├── portifolio/          # Vazio (remover)
└── services/            # APIs externas
```

---

## 2. Problemas Identificados

### 2.1 Backend

| Severidade | Problema | Impacto |
|------------|----------|---------|
| CRITICO | DEBUG=True em producao | Seguranca |
| CRITICO | SECRET_KEY exposta | Seguranca |
| CRITICO | Token API hardcoded | Seguranca |
| CRITICO | Views sem autenticacao | Seguranca |
| CRITICO | N+1 queries | Performance |
| CRITICO | Sem paginacao | Performance |
| CRITICO | Sem testes | Qualidade |
| ALTO | Sem indices em FKs | Performance |
| ALTO | Sem cache | Performance |
| ALTO | Sem logging | Observabilidade |
| MEDIO | SQLite em producao | Escalabilidade |
| MEDIO | Sem API REST | Extensibilidade |

### 2.2 Frontend

| Severidade | Problema | Impacto |
|------------|----------|---------|
| ALTO | Sem identidade visual | UX |
| ALTO | Paleta monocromatica | UX |
| ALTO | Sem tema escuro | UX |
| ALTO | Responsividade limitada | UX |
| MEDIO | Formularios basicos | UX |
| MEDIO | Sem microinteracoes | UX |
| MEDIO | Sem estados de loading | UX |

---

## 3. Visao do Produto

### 3.1 Objetivos

1. **Seguranca:** Sistema protegido com autenticacao e configuracoes seguras
2. **Performance:** Tempo de resposta < 500ms com cache e queries otimizadas
3. **Qualidade:** Cobertura de testes >= 80%
4. **UX:** Interface moderna, responsiva e acessivel
5. **Escalabilidade:** Arquitetura preparada para crescimento

### 3.2 Personas

- **Investidor Individual:** Gerencia portfolio pessoal de investimentos
- **Desenvolvedor:** Mantem e evolui o sistema

---

## 4. Epicos e Sprints

### 4.1 Visao Geral

```
┌─────────────────────────────────────────────────────────────────┐
│                    ROADMAP DE IMPLEMENTACAO                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SPRINT 1 ──► SPRINT 2 ──► SPRINT 3 ──► SPRINT 4 ──► SPRINT 5  │
│  Seguranca    Performance   Frontend     CRUD         Polish     │
│  & Config     & Database    Foundation   Redesign     & Deploy   │
│                                                                  │
│  [████████]   [████████]   [████████]   [████████]   [████████] │
│   2 semanas    2 semanas    2 semanas    2 semanas    1 semana   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Resumo de Sprints

| Sprint | Foco | Duracao | Story Points |
|--------|------|---------|--------------|
| Sprint 1 | Seguranca e Configuracao | 2 semanas | 34 pts |
| Sprint 2 | Performance e Database | 2 semanas | 29 pts |
| Sprint 3 | Frontend Foundation | 2 semanas | 34 pts |
| Sprint 4 | CRUD Redesign | 2 semanas | 29 pts |
| Sprint 5 | Polish e Deploy | 1 semana | 18 pts |
| **Total** | | **9 semanas** | **144 pts** |

---

## 5. Sprint Backlog Detalhado



## Historico de Versoes

| Versao | Data | Autor | Mudancas |
|--------|------|-------|----------|
| 1.0 | 29/01/2026 | Claude AI | Versao inicial (frontend) |
| 2.0 | 29/01/2026 | Claude AI | Adicao django-tailwind |
| 3.0 | 29/01/2026 | Claude AI | Unificacao frontend+backend em sprints |

---

**Documento aprovado por:** Product Owner
**Data de aprovacao:** 29/01/2026
**Proxima revisao:** Apos Sprint 3
