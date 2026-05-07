# SauceFlow E2E — E-Commerce Automation Hub

Automação E2E de e-commerce usando Flask (backend) + Playwright (robô) sobre o site SauceDemo.

## O que o projeto faz

O usuário digita um produto e um preço máximo. Um robô Playwright faz login no SauceDemo, coleta todos os produtos, filtra por nome e preço, exibe os resultados numa tabela e executa o checkout completo ao clicar em Comprar. Ao final salva um screenshot da confirmação.

## Fluxo das telas

```
[index.html]       → usuário digita item + preço máximo
      ↓
[/loading]         → tela intermediária com frases animadas (polling a cada 2s)
      ↓
[/resultados]      → tabela de produtos (o mais barato tem badge)
      ↓
[/checkout-status] → confirmação da compra + screenshot do SauceDemo
```

## Estrutura de pastas

```
ecommerce-automation-hub/
├── app.py                        # Flask app, logs JSON, rotas de tela
├── requirements.txt
├── .env                          # Credenciais SauceDemo (não vai pro git)
├── api/
│   └── routes.py                 # /run-search, /status/<id>, /run-checkout
├── automation/
│   ├── browser_manager.py        # Abre/fecha browser Playwright
│   ├── selectors.py              # Seletores CSS do SauceDemo
│   └── actions.py                # click, fill, get_all_elements com wait
├── services/
│   ├── search_service.py         # Login → coleta produtos → filtra → ordena
│   └── purchase_service.py       # Login → carrinho → checkout → screenshot
├── domain/
│   └── models.py                 # Product, Cart, Order
├── templates/
│   ├── index.html
│   ├── loading.html
│   ├── resultados.html
│   └── checkout.html
└── static/
    ├── css/style.css
    ├── js/loading.js              # Polling de status + rotação de frases
    ├── js/cart.js                 # Tabela de produtos + chamada de checkout
    └── screenshots/               # PNGs gerados pelo Playwright (gitkeep)
```

## Como rodar

```
cd ecommerce-automation-hub
python app.py
```

Acesse `http://127.0.0.1:5002` no browser.

> A porta está em 5002 porque 5000 e 5001 estão ocupadas por outros projetos na máquina do dev.

## Status das fases

| Fase | Descrição | Status |
|------|-----------|--------|
| 1 | domain/models.py — Product, Cart, Order | ✓ completo |
| 2 | automation/ — browser, selectors, actions | ✓ completo |
| 3 | services/ — search e purchase | ✓ completo |
| 4 | api/routes.py — endpoints Flask | ✓ completo |
| 5 | templates/ + static/js/ — todas as telas | ✓ completo |
| 6 | Integração completa + logs JSON estruturados | ✓ completo |
| 7 | Testes + README | pendente |

## Pendências

- **Fase 7:** escrever testes unitários (`tests/test_unit.py`) e E2E (`tests/test_e2e.py`) + README.md + ai_usage.md + readme_ai_bugs.md + test_output.md + screenshot de confirmação de compra

### Critérios dos testes (requisito do avaliador)

**Testes unitários — `tests/test_unit.py`:**
- Normalização de preço do produto: garantir que `price` chega como `float` (não string) e com moeda correta
- Política de seleção de produto: qual produto é escolhido dado um conjunto de resultados filtrados
- Cálculo do carrinho: total de itens e valor (se o modelo Cart implementar isso)

**Testes E2E — `tests/test_e2e.py`:**
- Pelo menos uma run completa do fluxo: Pesquisa → Adicionar ao carrinho → Checkout → Success
- O teste **deve obrigatoriamente** gerar um screenshot da tela de confirmação de compra
- **Pós-fase 7:** traduzir toda a UI para inglês (templates + JS)
- **Pós-fase 7:** melhorar o design (CSS)

## Observações técnicas

- O robô roda em thread separada; o frontend faz polling a cada 2s no `/status/<id>`
- Screenshots são salvas com caminho absoluto em `static/screenshots/` e servidas pelo Flask
- Logs são JSON estruturado com `ts`, `level`, `logger`, `requestId`, `step`, `duration_seconds`
- Playwright usa `_playwright_registry` para evitar que o GC encerre o servidor cedo
- SauceDemo não tem busca nativa — o robô coleta todos os produtos e filtra no Python
