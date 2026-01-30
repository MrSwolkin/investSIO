# UI Components - InvestSIO Design System

Base UI components library for the InvestSIO Django application.

## Overview

This directory contains reusable UI components built with Django Template Language (DTL) and TailwindCSS. All components follow the design system defined in `theme/static_src/src/styles.css` and integrate seamlessly with Alpine.js for interactivity.

## Components Reference

### T-018.1: Button (`_button.html`)

Flexible button component with multiple variants and sizes.

**Parameters:**
- `text` - Button text (string)
- `href` - Optional link URL (makes it an `<a>` tag)
- `variant` - Button style: `primary`|`success`|`danger`|`secondary`|`ghost` (default: `primary`)
- `size` - Button size: `sm`|`md`|`lg` (default: `md`)
- `icon` - Optional Bootstrap Icon class (e.g., `"bi-plus-circle"`)
- `type` - Button type for forms (default: `button`)
- `disabled` - Boolean to disable button
- `class` - Additional CSS classes

**Examples:**
```django
{# Primary button #}
{% include "components/ui/_button.html" with text="Salvar" variant="primary" %}

{# Success button with icon #}
{% include "components/ui/_button.html" with text="Criar Novo" variant="success" icon="bi-plus-circle" %}

{# Link button #}
{% include "components/ui/_button.html" with text="Ver Detalhes" href="/tickers/1/details/" %}

{# Small danger button #}
{% include "components/ui/_button.html" with text="Excluir" variant="danger" size="sm" icon="bi-trash" %}

{# Submit button for forms #}
{% include "components/ui/_button.html" with text="Enviar" variant="primary" type="submit" %}

{# Icon-only ghost button #}
{% include "components/ui/_button.html" with icon="bi-pencil" variant="ghost" size="sm" class="btn-icon" %}
```

---

### T-018.2: Card (`_card.html`)

Card container with optional header and footer sections.

**Parameters:**
- `title` - Card header title (optional)
- `subtitle` - Card subtitle in header (optional)
- `footer` - Show footer section (boolean, optional)
- `hover` - Add hover effect (boolean, optional)
- `class` - Additional CSS classes

**Blocks:**
- `card_body` - Main card content
- `card_footer` - Footer content

**Examples:**
```django
{# Simple card with title #}
{% include "components/ui/_card.html" with title="Resumo do Portfolio" %}
  <p>Conteúdo do card aqui...</p>

{# Card with title and subtitle #}
{% include "components/ui/_card.html" with title="Ticker PETR4" subtitle="Petrobras PN" %}
  <p>Informações do ticker...</p>

{# Card with hover effect #}
{% include "components/ui/_card.html" with title="Dashboard" hover=True %}
  <p>Card com efeito hover...</p>
```

---

### T-018.3: Metric Card (`_metric_card.html`)

Dashboard metric card with gradient backgrounds and optional change indicators.

**Parameters:**
- `value` - The main metric value (required, e.g., `"R$ 125.450,00"`)
- `label` - Description label (required, e.g., `"Patrimônio Total"`)
- `icon` - Bootstrap Icon class (e.g., `"bi-wallet2"`)
- `variant` - Gradient color: `primary`|`success`|`danger` (default: `primary`)
- `change` - Optional percentage change (e.g., `"+5.2%"`)
- `change_positive` - Boolean indicating positive change (default: `true`)
- `class` - Additional CSS classes

**Examples:**
```django
{# Basic metric card #}
{% include "components/ui/_metric_card.html" with value="R$ 125.450,00" label="Patrimônio Total" icon="bi-wallet2" %}

{# Success variant with positive change #}
{% include "components/ui/_metric_card.html" with value="R$ 8.320,50" label="Rendimentos" icon="bi-graph-up-arrow" variant="success" change="+12.5%" change_positive=True %}

{# Danger variant with negative change #}
{% include "components/ui/_metric_card.html" with value="R$ -2.150,00" label="Prejuízo" icon="bi-graph-down-arrow" variant="danger" change="-3.2%" change_positive=False %}
```

---

### T-018.4: Badge (`_badge.html`)

Small badge component for labels and status indicators.

**Parameters:**
- `text` - Badge text (required)
- `variant` - Badge style: `primary`|`success`|`danger`|`warning`|`neutral` (default: `neutral`)
- `icon` - Optional Bootstrap Icon class
- `class` - Additional CSS classes

**Examples:**
```django
{# Neutral badge #}
{% include "components/ui/_badge.html" with text="Ativo" %}

{# Success badge with icon #}
{% include "components/ui/_badge.html" with text="Aprovado" variant="success" icon="bi-check-circle" %}

{# Danger badge #}
{% include "components/ui/_badge.html" with text="Cancelado" variant="danger" icon="bi-x-circle" %}

{# Warning badge #}
{% include "components/ui/_badge.html" with text="Pendente" variant="warning" icon="bi-clock" %}
```

---

### T-018.5: Table (`_table.html`)

Responsive table wrapper with consistent styling.

**Parameters:**
- `headers` - List of table header labels (optional)
- `class` - Additional CSS classes

**Blocks:**
- `table_header` - Custom header row
- `table_body` - Table body content

**Examples:**
```django
{# Table with predefined structure #}
<div class="overflow-x-auto rounded-xl border border-border-default">
  <table class="table">
    <thead>
      <tr>
        <th>Ticker</th>
        <th>Quantidade</th>
        <th>Preço</th>
      </tr>
    </thead>
    <tbody>
      {% for item in items %}
        <tr>
          <td>{{ item.ticker }}</td>
          <td>{{ item.quantity }}</td>
          <td>{{ item.price }}</td>
        </tr>
      {% endfor %}
    </tbody>
  </table>
</div>
```

---

### T-018.6: Modal (`_modal.html`)

Modal dialog with Alpine.js for interactivity.

**Parameters:**
- `id` - Unique modal identifier (required)
- `title` - Modal header title (required)
- `size` - Modal size: `sm`|`md`|`lg` (default: `md`)
- `class` - Additional CSS classes

**Blocks:**
- `modal_body` - Main modal content
- `modal_footer` - Footer with action buttons

**Important:** Wrap modal in Alpine.js `x-data` context with boolean state.

**Examples:**
```django
{# Basic modal with trigger #}
<div x-data="{ showModal: false }">
  <!-- Trigger Button -->
  <button @click="showModal = true" class="btn btn-primary">
    Abrir Modal
  </button>

  <!-- Modal -->
  <template x-if="showModal">
    {% include "components/ui/_modal.html" with id="example" title="Confirmar Ação" %}
      <!-- Note: Due to DTL limitations, pass content via variables or custom template -->
  </template>
</div>

{# Large modal #}
<div x-data="{ detailsModal: false }">
  <button @click="detailsModal = true" class="btn btn-primary">Ver Detalhes</button>

  <template x-if="detailsModal">
    {% include "components/ui/_modal.html" with id="details" title="Detalhes do Ativo" size="lg" %}
  </template>
</div>
```

---

### T-018.7: Alert (`_alert.html`)

Alert/notification component with auto-dismiss functionality.

**Parameters:**
- `message` - Alert message text (required)
- `variant` - Alert style: `info`|`success`|`warning`|`danger` (default: `info`)
- `dismissible` - Show close button (boolean, default: `false`)
- `icon` - Optional Bootstrap Icon (auto-selected based on variant if not provided)
- `auto_dismiss` - Auto-dismiss after 5 seconds (boolean, default: `false`)
- `class` - Additional CSS classes

**Examples:**
```django
{# Info alert #}
{% include "components/ui/_alert.html" with message="Informação importante sobre o sistema." variant="info" %}

{# Success alert with dismissible #}
{% include "components/ui/_alert.html" with message="Operação realizada com sucesso!" variant="success" dismissible=True %}

{# Warning alert #}
{% include "components/ui/_alert.html" with message="Atenção: verifique os dados antes de continuar." variant="warning" dismissible=True %}

{# Danger alert with auto-dismiss #}
{% include "components/ui/_alert.html" with message="Erro ao processar a requisição." variant="danger" dismissible=True auto_dismiss=True %}
```

---

### T-018.8: Empty State (`_empty_state.html`)

Empty state component for when no data is available.

**Parameters:**
- `icon` - Bootstrap Icon class (required)
- `title` - Main message (required)
- `description` - Secondary descriptive text (optional)
- `action_text` - Optional button text
- `action_href` - Optional button link URL
- `action_variant` - Button variant (default: `primary`)
- `class` - Additional CSS classes

**Examples:**
```django
{# Basic empty state #}
{% include "components/ui/_empty_state.html" with icon="bi-inbox" title="Nenhum item encontrado" description="Não há dados para exibir no momento." %}

{# Empty state with action button #}
{% include "components/ui/_empty_state.html" with icon="bi-folder-plus" title="Nenhuma corretora cadastrada" description="Comece criando sua primeira corretora para gerenciar seus investimentos." action_text="Criar Corretora" action_href="/brokers/create/" %}

{# Empty search results #}
{% include "components/ui/_empty_state.html" with icon="bi-search" title="Nenhum resultado encontrado" description="Tente ajustar seus filtros de busca." %}
```

---

## Design System Integration

All components use classes from `/theme/static_src/src/styles.css`:

### Colors
- Background: `bg-bg-base`, `bg-bg-surface`, `bg-bg-elevated`
- Text: `text-text-primary`, `text-text-secondary`, `text-text-muted`
- Brand: `bg-brand-primary`, `bg-brand-success`, `bg-brand-danger`, `bg-brand-warning`
- Border: `border-border-default`, `border-border-focus`

### Typography
- Display Font: `font-display` (Poppins)
- Body Font: `font-sans` (Inter)

### Animations
- `animate-fade-in`, `animate-fade-out`
- `animate-slide-up`, `animate-slide-down`
- `animate-scale-in`
- `animate-pulse-soft`, `animate-shimmer`

### Component Classes
- Buttons: `.btn`, `.btn-primary`, `.btn-success`, `.btn-danger`, `.btn-secondary`, `.btn-ghost`
- Button Sizes: `.btn-sm`, `.btn-lg`, `.btn-icon`
- Cards: `.card`, `.card-header`, `.card-body`, `.card-footer`, `.card-hover`
- Metrics: `.metric-card`, `.metric-card-gradient-*`, `.metric-value`, `.metric-label`
- Badges: `.badge`, `.badge-primary`, `.badge-success`, `.badge-danger`, `.badge-warning`, `.badge-neutral`
- Tables: `.table`
- Alerts: `.alert`, `.alert-info`, `.alert-success`, `.alert-warning`, `.alert-danger`
- Modals: `.modal-backdrop`, `.modal`, `.modal-content`, `.modal-header`, `.modal-body`, `.modal-footer`
- Empty State: `.empty-state`, `.empty-state-icon`, `.empty-state-title`, `.empty-state-description`

## Best Practices

### 1. Component Reusability
Always use components instead of repeating HTML structure:

```django
{# Bad #}
<button class="btn btn-primary">
  <i class="bi bi-plus"></i>
  Criar
</button>

{# Good #}
{% include "components/ui/_button.html" with text="Criar" variant="primary" icon="bi-plus" %}
```

### 2. Accessibility
- All interactive elements have proper `aria-label` attributes
- Focus states are visible and consistent
- Color contrast meets WCAG standards
- Semantic HTML is used throughout

### 3. Alpine.js Integration
Components requiring interactivity use Alpine.js:
- Modals use `x-show`, `x-data`, and `x-transition`
- Alerts use `x-show` for dismissible functionality
- Always initialize Alpine.js state in parent container

### 4. Responsive Design
All components are mobile-first and responsive:
- Tables use `.overflow-x-auto` wrapper for horizontal scroll
- Modals adjust to viewport with `max-w-*` and padding
- Grid layouts use responsive breakpoints

### 5. Customization
Extend components with the `class` parameter:

```django
{% include "components/ui/_button.html" with text="Custom" class="w-full mt-4" %}
```

## Icons

Bootstrap Icons are available project-wide. Common icons:

- **Actions:** `bi-plus`, `bi-pencil`, `bi-trash`, `bi-search`, `bi-filter`
- **Status:** `bi-check-circle`, `bi-x-circle`, `bi-exclamation-triangle`, `bi-info-circle`
- **Navigation:** `bi-arrow-left`, `bi-arrow-right`, `bi-chevron-down`, `bi-house`
- **Finance:** `bi-wallet2`, `bi-graph-up-arrow`, `bi-graph-down-arrow`, `bi-currency-dollar`
- **Data:** `bi-table`, `bi-bar-chart`, `bi-pie-chart`, `bi-list-ul`
- **Files:** `bi-folder`, `bi-file-text`, `bi-download`, `bi-upload`

Full icon list: https://icons.getbootstrap.com/

## Development Workflow

1. **Use existing components** whenever possible
2. **Extend with parameters** before creating new components
3. **Follow naming conventions**: `_component_name.html`
4. **Document thoroughly** with usage examples in comments
5. **Test responsiveness** on mobile, tablet, and desktop
6. **Validate accessibility** with keyboard navigation and screen readers

## Support

For issues or questions about components, refer to:
- Design system: `/theme/static_src/src/styles.css`
- Base template: `/app/templates/base.html`
- Existing implementations: `/app/templates/home.html`

---

**Version:** Sprint 3 - US-018
**Last Updated:** 2026-01-30
