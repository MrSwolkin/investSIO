# UX/UI Improvements - InvestSIO

## Análise e Recomendações de Melhorias

> Documento gerado com base nas melhores práticas de UX/UI do mercado para aplicações financeiras.

---

## Sumário

1. [Análise do Estado Atual](#1-análise-do-estado-atual)
2. [Melhorias de UX](#2-melhorias-de-ux)
3. [Melhorias de UI](#3-melhorias-de-ui)
4. [Acessibilidade](#4-acessibilidade)
5. [Performance Percebida](#5-performance-percebida)
6. [Mobile-First & Responsividade](#6-mobile-first--responsividade)
7. [Padrões de Design Financeiro](#7-padrões-de-design-financeiro)
8. [Priorização](#8-priorização)

---

## 1. Análise do Estado Atual

### Pontos Positivos ✅
- Design system com TailwindCSS v4 bem estruturado
- Paleta de cores consistente (dark theme)
- Componentização de templates Django
- Dashboard com métricas principais visíveis
- Sistema de autenticação funcional

### Áreas de Melhoria 🔧
- Navegação não otimizada para mobile
- Feedback visual limitado em ações do usuário
- Ausência de estados vazios (empty states)
- Falta de onboarding para novos usuários
- Gráficos sem interatividade
- Formulários longos sem progressão visual

---

## 2. Melhorias de UX

### 2.1 Navegação e Arquitetura de Informação

| Item | Problema | Solução | Impacto |
|------|----------|---------|---------|
| Menu Principal | Navegação linear sem hierarquia | Implementar navegação contextual com breadcrumbs | Alto |
| Quick Actions | Ações frequentes exigem múltiplos cliques | Adicionar FAB (Floating Action Button) para ações rápidas | Alto |
| Busca Global | Inexistente | Implementar search bar com sugestões (tickers, brokers) | Médio |
| Atalhos de Teclado | Não implementados | Adicionar shortcuts para power users (Cmd+K para busca) | Baixo |

### 2.2 Fluxos de Usuário

#### Fluxo de Registro de Compra (Inflow)
```
ATUAL:
Home → Menu → Inflows → List → Create → Formulário longo → Submit

PROPOSTO:
Home → FAB (+) → Modal rápido com campos essenciais → Submit
        ↓
      Opção "Mais detalhes" → Formulário completo
```

#### Fluxo de Visualização de Portfólio
```
ATUAL:
Dashboard genérico → Navegação manual para cada seção

PROPOSTO:
Dashboard personalizado → Cards clicáveis com drill-down
        ↓
      Filtros persistentes → Visualizações salvas
```

### 2.3 Estados e Feedback

- [ ] **Empty States**: Criar telas para quando não há dados
  - Primeira compra: Guia ilustrado de como começar
  - Sem dividendos: Explicação e sugestões de ativos

- [ ] **Loading States**: Implementar skeletons em vez de spinners

- [ ] **Success/Error States**: Toasts animados com ações de undo

- [ ] **Offline State**: Indicador de conectividade e cache local

### 2.4 Onboarding

```
Passo 1: Boas-vindas + Configuração de moeda base
    ↓
Passo 2: Cadastro da primeira corretora
    ↓
Passo 3: Registro do primeiro ativo
    ↓
Passo 4: Tour guiado pelo dashboard
    ↓
Passo 5: Checklist de "Próximos passos"
```

### 2.5 Micro-interações

| Elemento | Interação Atual | Proposta |
|----------|-----------------|----------|
| Botões | Clique simples | Ripple effect + feedback háptico (mobile) |
| Cards | Estáticos | Hover com elevação + preview de dados |
| Gráficos | Estáticos | Tooltips interativos + zoom |
| Tabelas | Scroll simples | Sticky headers + ordenação visual |
| Formulários | Submit único | Validação em tempo real + auto-save |

---

## 3. Melhorias de UI

### 3.1 Sistema de Design Aprimorado

#### Tipografia
```css
/* Hierarquia atual limitada - Proposta: */
--font-display: 'Poppins', sans-serif;  /* Títulos */
--font-body: 'Inter', sans-serif;        /* Corpo */
--font-mono: 'JetBrains Mono', monospace; /* Valores financeiros */

/* Escala tipográfica */
--text-xs: 0.75rem;   /* 12px - Labels */
--text-sm: 0.875rem;  /* 14px - Captions */
--text-base: 1rem;    /* 16px - Body */
--text-lg: 1.125rem;  /* 18px - Subheadings */
--text-xl: 1.25rem;   /* 20px - Headings */
--text-2xl: 1.5rem;   /* 24px - Page titles */
--text-3xl: 2rem;     /* 32px - Hero numbers */
```

#### Paleta de Cores Expandida
```css
/* Cores semânticas para finanças */
--color-profit: #10b981;      /* Verde - Lucro */
--color-profit-bg: #10b98115; /* Verde transparente */
--color-loss: #ef4444;        /* Vermelho - Prejuízo */
--color-loss-bg: #ef444415;   /* Vermelho transparente */
--color-neutral: #6b7280;     /* Cinza - Neutro */
--color-dividend: #8b5cf6;    /* Roxo - Dividendos */
--color-info: #3b82f6;        /* Azul - Informativo */

/* Categorias de ativos */
--color-fii: #f59e0b;         /* Laranja - FIIs */
--color-acao: #3b82f6;        /* Azul - Ações */
--color-stock: #10b981;       /* Verde - Stocks */
--color-etf: #8b5cf6;         /* Roxo - ETFs */
--color-crypto: #ec4899;      /* Rosa - Crypto (futuro) */
```

### 3.2 Componentes Novos

#### Card de Métrica Aprimorado
```html
<!-- Proposta de novo card com variação -->
<div class="metric-card">
  <div class="metric-header">
    <span class="metric-label">Total Investido</span>
    <span class="metric-badge positive">+12.5%</span>
  </div>
  <div class="metric-value">R$ 125.430,00</div>
  <div class="metric-chart">
    <!-- Sparkline de 30 dias -->
  </div>
  <div class="metric-footer">
    <span class="metric-comparison">vs. mês anterior: +R$ 5.200</span>
  </div>
</div>
```

#### Tabela Aprimorada
```html
<!-- Tabela com filtros inline e ações rápidas -->
<table class="data-table">
  <thead>
    <tr>
      <th class="sortable">Ativo <icon-sort/></th>
      <th class="filterable">Categoria <icon-filter/></th>
      <th class="numeric">Quantidade</th>
      <th class="numeric highlight">P/L</th>
      <th class="actions">Ações</th>
    </tr>
  </thead>
  <!-- Linhas com cores condicionais baseadas em P/L -->
</table>
```

### 3.3 Iconografia

| Contexto | Ícone Atual | Proposta |
|----------|-------------|----------|
| Compra | Genérico | Arrow-down-circle (verde) |
| Venda | Genérico | Arrow-up-circle (vermelho) |
| Dividendo | Genérico | Coins / Banknotes |
| FII | Texto | Building-office |
| Ação BR | Texto | Flag-br + Chart-line |
| Stock US | Texto | Flag-us + Chart-line |
| Lucro | Texto | Trending-up (verde) |
| Prejuízo | Texto | Trending-down (vermelho) |

**Biblioteca recomendada**: Heroicons ou Lucide (já usado no ballet-content-builder)

### 3.4 Animações e Transições

```css
/* Padrão de animação suave */
--transition-fast: 150ms ease-out;
--transition-normal: 250ms ease-out;
--transition-slow: 350ms ease-out;

/* Animações de entrada */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideInRight {
  from { opacity: 0; transform: translateX(20px); }
  to { opacity: 1; transform: translateX(0); }
}

/* Aplicação em cards */
.metric-card {
  animation: fadeInUp var(--transition-normal);
  animation-delay: calc(var(--card-index) * 50ms);
}
```

---

## 4. Acessibilidade

### 4.1 WCAG 2.1 AA Compliance

- [ ] **Contraste de cores**: Verificar ratio mínimo 4.5:1 para texto
- [ ] **Foco visível**: Outline claro em todos elementos interativos
- [ ] **Alt text**: Descrições em gráficos e imagens
- [ ] **ARIA labels**: Em botões de ícone e elementos interativos
- [ ] **Skip links**: Navegação rápida para conteúdo principal
- [ ] **Tamanho de toque**: Mínimo 44x44px em mobile

### 4.2 Daltonismo

```css
/* Não depender apenas de cor para indicar lucro/prejuízo */
.profit {
  color: var(--color-profit);
  /* Adicionar ícone ou texto complementar */
}
.profit::before { content: '▲ '; }

.loss {
  color: var(--color-loss);
}
.loss::before { content: '▼ '; }
```

### 4.3 Leitor de Tela

```html
<!-- Exemplo de tabela acessível -->
<table role="grid" aria-label="Portfólio de investimentos">
  <caption class="sr-only">
    Lista de ativos com quantidade, preço médio e variação
  </caption>
  <!-- ... -->
</table>
```

---

## 5. Performance Percebida

### 5.1 Skeleton Loading

```html
<!-- Durante carregamento de dados -->
<div class="metric-card skeleton">
  <div class="skeleton-line w-1/3"></div>
  <div class="skeleton-line w-2/3 h-8"></div>
  <div class="skeleton-chart"></div>
</div>
```

### 5.2 Otimizações

| Técnica | Implementação | Benefício |
|---------|---------------|-----------|
| Lazy Loading | Carregar gráficos sob demanda | -40% tempo inicial |
| Image Optimization | WebP + lazy loading | -60% tamanho |
| Code Splitting | Separar JS por rota | -30% bundle |
| Prefetch | Links de navegação | Transições instantâneas |
| Service Worker | Cache de assets | Funciona offline |

### 5.3 Indicadores de Progresso

```
Ação rápida (< 1s):      Nenhum indicador
Ação média (1-3s):       Spinner no botão
Ação longa (> 3s):       Progress bar + mensagem
Ação muito longa (> 10s): Progress bar + estimativa + cancelar
```

---

## 6. Mobile-First & Responsividade

### 6.1 Breakpoints

```css
/* TailwindCSS v4 breakpoints */
--breakpoint-sm: 640px;   /* Celular landscape */
--breakpoint-md: 768px;   /* Tablet portrait */
--breakpoint-lg: 1024px;  /* Tablet landscape / Desktop pequeno */
--breakpoint-xl: 1280px;  /* Desktop */
--breakpoint-2xl: 1536px; /* Desktop grande */
```

### 6.2 Layout Adaptativo

| Componente | Mobile | Tablet | Desktop |
|------------|--------|--------|---------|
| Dashboard | Stack vertical | Grid 2 colunas | Grid 3-4 colunas |
| Tabelas | Cards empilhados | Tabela compacta | Tabela completa |
| Navegação | Bottom tabs | Sidebar colapsável | Sidebar fixa |
| Gráficos | Scrollable | Fit container | Multi-chart view |
| Forms | Full width | 2 colunas | 3 colunas |

### 6.3 Gestos Mobile

| Gesto | Ação |
|-------|------|
| Pull-to-refresh | Atualizar cotações |
| Swipe left | Revelar ações (editar/deletar) |
| Swipe right | Marcar como favorito |
| Long press | Menu de contexto |
| Pinch zoom | Ampliar gráficos |

---

## 7. Padrões de Design Financeiro

### 7.1 Formatação de Números

```javascript
// Valores monetários
formatCurrency(125430.50, 'BRL') // → R$ 125.430,50
formatCurrency(1000.00, 'USD')   // → US$ 1,000.00

// Percentuais
formatPercent(0.125)    // → 12,50%
formatPercent(-0.034)   // → -3,40%

// Variações com cor
formatChange(0.125)     // → +12,50% (verde)
formatChange(-0.034)    // → -3,40% (vermelho)

// Quantidades de ações
formatQuantity(1500)    // → 1.500
formatQuantity(0.5)     // → 0,50 (frações)
```

### 7.2 Visualização de Dados

| Métrica | Tipo de Gráfico | Justificativa |
|---------|-----------------|---------------|
| Distribuição por categoria | Donut chart | Proporções claras |
| Evolução patrimonial | Area chart | Tendência + volume |
| Dividendos mensais | Bar chart | Comparação discreta |
| Rentabilidade | Line chart | Tendência temporal |
| Comparativo brokers | Horizontal bar | Ranking |

### 7.3 Alertas e Notificações

```
🔔 Tipos de alertas:

[INFO] Dividendo recebido: MXRF11 - R$ 45,00
[SUCCESS] Compra registrada: 100 PETR4 @ R$ 35,50
[WARNING] Ativo com baixa liquidez: XXXX11
[ERROR] Falha ao atualizar cotações
[REMINDER] Dividendo declarado: HGLG11 - Pgto em 15/02
```

---

## 8. Priorização

### 8.1 Matriz de Impacto x Esforço

```
                    ALTO IMPACTO
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
    │  QUICK WINS        │  BIG BETS          │
    │  • Empty states    │  • Onboarding      │
    │  • Skeleton load   │  • Mobile nav      │
    │  • Toasts          │  • Gráficos inter. │
    │  • Formatação      │  • Busca global    │
    │                    │                    │
────┼────────────────────┼────────────────────┼────
    │                    │                    │
    │  FILL-INS          │  MONEY PITS        │
    │  • Atalhos teclado │  • Animações       │
    │  • Breadcrumbs     │  • Gestos mobile   │
    │  • Tooltips        │  • PWA offline     │
    │                    │                    │
    └────────────────────┼────────────────────┘
                         │
                   BAIXO IMPACTO

   BAIXO ESFORÇO ←───────┼───────→ ALTO ESFORÇO
```

### 8.2 Roadmap de Implementação

#### Sprint 1-2: Quick Wins
- [ ] Empty states para todas as listas
- [ ] Skeleton loading no dashboard
- [ ] Sistema de toasts
- [ ] Formatação de números padronizada
- [ ] Cores semânticas (profit/loss)

#### Sprint 3-4: Experiência Base
- [ ] Navegação mobile (bottom tabs)
- [ ] FAB para ações rápidas
- [ ] Formulários com validação em tempo real
- [ ] Breadcrumbs

#### Sprint 5-6: Engajamento
- [ ] Onboarding flow
- [ ] Gráficos interativos
- [ ] Busca global
- [ ] Notificações de dividendos

#### Sprint 7-8: Polish
- [ ] Animações e transições
- [ ] Gestos mobile
- [ ] Modo offline (PWA)
- [ ] Acessibilidade completa

---

## Referências

- [Material Design 3](https://m3.material.io/)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [FinTech Design System - Plaid](https://plaid.com/docs/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Nielsen Norman Group - Financial UX](https://www.nngroup.com/articles/financial-ux/)

---

*Documento atualizado em: Fevereiro 2026*
