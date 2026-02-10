# Design System

Sistema de design do InvestSIO usando TailwindCSS v4.

## Visao Geral

O design system do InvestSIO e baseado em:
- **TailwindCSS v4** com configuracao via CSS
- **Tema escuro** como padrao
- **Componentes reutilizaveis** via Django templates
- **Acessibilidade** WCAG AA

## Paleta de Cores

### Cores de Background

| Token | Hex | Uso |
|-------|-----|-----|
| `bg-base` | `#0f172a` | Background principal (slate-900) |
| `bg-surface` | `#1e293b` | Cards, modais (slate-800) |
| `bg-elevated` | `#334155` | Hover states (slate-700) |

### Cores de Texto

| Token | Hex | Uso |
|-------|-----|-----|
| `text-primary` | `#f1f5f9` | Titulos (slate-100) |
| `text-secondary` | `#cbd5e1` | Labels (slate-300) |
| `text-muted` | `#94a3b8` | Placeholders (slate-400) |

### Cores de Marca

| Token | Hex | Uso |
|-------|-----|-----|
| `brand-primary` | `#3b82f6` | CTAs principais (blue-500) |
| `brand-secondary` | `#06b6d4` | Secundario (cyan-500) |
| `brand-success` | `#10b981` | Compras, positivo (emerald-500) |
| `brand-danger` | `#ef4444` | Vendas, negativo (red-500) |
| `brand-warning` | `#f59e0b` | Alertas (amber-500) |

### Cores de Borda

| Token | Hex | Uso |
|-------|-----|-----|
| `border-default` | `#334155` | Bordas padrao (slate-700) |
| `border-focus` | `#3b82f6` | Focus ring (blue-500) |

## Tipografia

### Fontes

```css
--font-sans: 'Inter', ui-sans-serif, system-ui, sans-serif;
--font-display: 'Poppins', ui-sans-serif, system-ui, sans-serif;
--font-mono: ui-monospace, SFMono-Regular, 'Consolas', monospace;
```

### Uso

- **Headings**: Poppins (font-display)
- **Body text**: Inter (font-sans)
- **Code/Values**: Monospace (font-mono)

## Gradientes

| Nome | Classes | Uso |
|------|---------|-----|
| Primary | `from-blue-500 to-cyan-500` | Botoes primarios |
| Success | `from-emerald-500 to-teal-500` | Compras, positivo |
| Danger | `from-red-500 to-pink-500` | Vendas, delecao |

## Componentes

### Buttons

```django
{% include "components/ui/_button.html" with
    text="Texto"
    variant="primary"       {# primary|success|danger|secondary|ghost #}
    size="md"               {# sm|md|lg #}
    icon="bi-plus"          {# Bootstrap Icon class #}
    href="/url/"            {# Se fornecido, renderiza como <a> #}
    disabled=True           {# Desabilita o botao #}
%}
```

**Variantes:**
- `primary`: Gradiente azul-ciano, sombra azul
- `success`: Gradiente verde-teal, sombra verde
- `danger`: Gradiente vermelho-pink, sombra vermelha
- `secondary`: Background cinza, borda
- `ghost`: Transparente, hover cinza

### Cards

```django
{% include "components/ui/_card.html" %}
    {% block card_header %}Titulo{% endblock %}
    {% block card_body %}Conteudo{% endblock %}
    {% block card_footer %}Rodape{% endblock %}
{% endinclude %}
```

**CSS Classes:**
- `.card`: Container principal
- `.card-header`: Cabecalho com borda inferior
- `.card-body`: Conteudo
- `.card-footer`: Rodape com borda superior
- `.card-hover`: Card com efeito hover

### Metric Cards

```django
{% include "components/ui/_metric_card.html" with
    value="R$ 1.000,00"     {# Valor principal #}
    label="Total Investido" {# Label da metrica #}
    icon="bi-wallet2"       {# Icone Bootstrap #}
    variant="success"       {# primary|success|danger #}
    change="+12.5%"         {# Indicador de mudanca #}
    change_positive=True    {# Direcao da mudanca #}
%}
```

### Badges

```django
{% include "components/ui/_badge.html" with
    text="Ativo"            {# Texto do badge #}
    variant="success"       {# primary|success|danger|warning|neutral #}
    icon="bi-check-circle"  {# Icone opcional #}
%}
```

### Tables

```django
{% include "components/ui/_table.html" with
    headers=header_list     {# Lista de cabecalhos #}
    caption="Descricao"     {# Caption para acessibilidade #}
%}
    {% block table_body %}
    <tr>
        <td>...</td>
    </tr>
    {% endblock %}
{% endinclude %}
```

### Modals

```django
{% include "components/ui/_modal.html" with
    id="modal-delete"       {# ID unico #}
    title="Confirmar"       {# Titulo do modal #}
    size="lg"               {# sm|md|lg #}
%}
    {% block modal_body %}Conteudo{% endblock %}
    {% block modal_footer %}Botoes{% endblock %}
{% endinclude %}
```

**Controle via Alpine.js:**
```javascript
// Abrir modal
Alpine.store('modals').open('modal-delete')

// Fechar modal
Alpine.store('modals').close('modal-delete')
```

### Alerts

```django
{% include "components/ui/_alert.html" with
    message="Mensagem"      {# Texto do alerta #}
    variant="success"       {# info|success|warning|danger #}
    dismissible=True        {# Permite fechar #}
%}
```

### Empty States

```django
{% include "components/ui/_empty_state.html" with
    icon="bi-inbox"         {# Icone grande #}
    title="Nenhum dado"     {# Titulo #}
    description="Texto"     {# Descricao #}
    action_text="Criar"     {# Texto do botao #}
    action_href="/create/"  {# URL do botao #}
%}
```

### Pagination

```django
{% include "components/_pagination.html" with
    page_obj=page_obj       {# Django page object #}
%}
```

## Form Components

### Form Field

```django
{% include "components/forms/_form_field.html" with
    field=form.name         {# Campo do form #}
    label="Nome"            {# Label customizado #}
    help_text="Ajuda"       {# Texto de ajuda #}
%}
```

### CSS Input Classes

- `.input`: Input padrao
- `.input-error`: Input com erro
- `.input-success`: Input valido
- `.select`: Select estilizado
- `.textarea`: Textarea estilizado
- `.checkbox`: Checkbox estilizado
- `.label`: Label padrao

## Animacoes

### Disponiveis

```css
--animate-fade-in: fade-in 0.3s ease-out;
--animate-fade-out: fade-out 0.3s ease-out;
--animate-slide-up: slide-up 0.3s ease-out;
--animate-slide-down: slide-down 0.3s ease-out;
--animate-scale-in: scale-in 0.2s ease-out;
--animate-pulse-soft: pulse-soft 2s ease-in-out infinite;
--animate-shimmer: shimmer 1.5s infinite;
```

### Uso

```html
<div class="animate-fade-in">Conteudo</div>
<div class="animate-slide-up">Conteudo</div>
```

## Loading Skeletons

```html
<div class="skeleton h-4 w-full"></div>
<div class="skeleton-text"></div>
<div class="skeleton-title"></div>
<div class="skeleton-avatar"></div>
<div class="skeleton-card"></div>
```

## Utilitarios

### Gradient Text

```html
<span class="text-gradient-primary">Texto com gradiente</span>
<span class="text-gradient-success">Texto verde</span>
<span class="text-gradient-danger">Texto vermelho</span>
```

### Scrollbar

```html
<div class="scrollbar-hide">Sem scrollbar visivel</div>
<div class="scrollbar-custom">Scrollbar personalizado</div>
```

### Glass Effect

```html
<div class="glass">Efeito vidro com blur</div>
```

### Line Clamp

```html
<p class="line-clamp-2">Trunca em 2 linhas</p>
<p class="line-clamp-3">Trunca em 3 linhas</p>
```

## Acessibilidade

### Focus Visible

Todos os elementos interativos tem estilo de foco visivel:

```css
:focus-visible {
  @apply outline-2 outline-offset-2 outline-brand-primary;
}
```

### ARIA Attributes

Os componentes incluem atributos ARIA:

- `role="dialog"` em modals
- `aria-modal="true"` em modals
- `aria-expanded` em dropdowns
- `aria-hidden="true"` em icones decorativos
- `aria-label` em botoes icon-only
- `scope="col"` em headers de tabela

### Skip Navigation

O template base inclui link para pular navegacao:

```html
<a href="#main-content" class="sr-only focus:not-sr-only">
    Pular para o conteudo
</a>
```

## Responsividade

### Breakpoints

```css
sm: 640px
md: 768px
lg: 1024px
xl: 1280px
2xl: 1536px
```

### Layout Padrao

- Mobile: Stack vertical
- Tablet (md): Grid 2 colunas
- Desktop (lg): Sidebar + Conteudo

## Icones

Usamos Bootstrap Icons via CDN:

```html
<i class="bi bi-plus-circle"></i>
<i class="bi bi-pencil-square"></i>
<i class="bi bi-trash3-fill"></i>
```

Documentacao: https://icons.getbootstrap.com/

## Arquivo de Configuracao

O design system e configurado em:
```
theme/static_src/src/styles.css
```

Este arquivo usa a sintaxe TailwindCSS v4 com `@theme` para tokens.
