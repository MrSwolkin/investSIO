# Agentes de IA - InvestSIO

Este diretorio contem os agentes de IA especializados para o desenvolvimento do projeto InvestSIO.

## Indice de Agentes

| Agente | Arquivo | Descricao |
|--------|---------|-----------|
| Backend Django | [backend-django.md](./backend-django.md) | Desenvolvimento backend com Django 6.0.1 |
| Frontend TailwindCSS | [frontend-tailwind.md](./frontend-tailwind.md) | Frontend com Django Templates e TailwindCSS |
| QA Tester | [qa-tester.md](./qa-tester.md) | Testes end-to-end com Playwright |
| Database | [database.md](./database.md) | Modelagem, migrations e otimizacao de queries |
| API Integration | [api-integration.md](./api-integration.md) | Integracao com APIs externas |

## Quando Usar Cada Agente

### Backend Django
Use quando precisar:
- Criar ou modificar models Django
- Implementar views (CBVs ou FBVs)
- Criar forms e validacoes
- Configurar URLs e settings
- Implementar autenticacao e autorizacao
- Adicionar logging e tratamento de erros
- Criar management commands

### Frontend TailwindCSS
Use quando precisar:
- Criar ou redesenhar templates Django
- Implementar componentes UI com TailwindCSS
- Adicionar interatividade com Alpine.js
- Integrar graficos com Chart.js
- Implementar responsividade e dark mode
- Criar formularios estilizados

### QA Tester
Use quando precisar:
- Validar fluxos de usuario end-to-end
- Verificar se o design esta correto
- Testar responsividade em diferentes dispositivos
- Identificar bugs visuais ou funcionais
- Validar acessibilidade
- Gerar relatorios de testes

### Database
Use quando precisar:
- Criar ou modificar models com indices
- Otimizar queries (N+1, select_related, prefetch_related)
- Criar migrations complexas
- Implementar validacoes de integridade
- Configurar cache

### API Integration
Use quando precisar:
- Integrar com BrAPI (dados de tickers)
- Integrar com BrasilAPI (taxas economicas)
- Implementar tratamento de erros de API
- Adicionar cache para requisicoes externas
- Criar novos servicos de integracao

## Stack do Projeto

| Tecnologia | Versao | Uso |
|------------|--------|-----|
| Python | 3.13 | Runtime |
| Django | 6.0.1 | Backend framework |
| TailwindCSS | 4.0.0 | Estilizacao (via django-tailwind) |
| Alpine.js | 3.x | Interatividade frontend |
| Chart.js | Latest | Graficos |
| SQLite/PostgreSQL | 3/Latest | Banco de dados |
| Playwright | Latest | Testes E2E |

## Uso dos MCP Servers

### Context7 (Documentacao)
Os agentes de implementacao tecnica (Backend, Frontend, Database, API) devem usar o MCP server do Context7 para:
- Buscar documentacao atualizada das tecnologias
- Garantir codigo baseado nas melhores praticas atuais
- Verificar APIs e metodos disponiveis

### Playwright (Testes)
O agente QA Tester deve usar o MCP server do Playwright para:
- Navegar pelo sistema
- Interagir com elementos da interface
- Capturar screenshots
- Validar comportamentos esperados
