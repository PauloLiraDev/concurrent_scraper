📖 Este README também está disponível em [English](./README.md)

# Concurrent Scraper API

API de web scraping concorrente construída com FastAPI e Selenium para extrair dados de produtos de sites web de forma eficiente.

## Comandos Básicos

### Executar a API

```bash

docker compose up -d --build

```

### Comandos de exemplo
```bash

curl -s 'http://localhost:8000/scrape'
curl -s 'http://localhost:8000/scrape?category=Electronics'

```

### Endpoints

#### Scrape de Produtos

**Todos os produtos:**
```
GET /scrape
```

**Produtos de uma categoria específica:**
```
GET /scrape?category=electronics
```

Categorias disponíveis:
- Apparel
- Cosmetics
- Electronics
- Home Goods

#### Documentação da API

```
GET /docs
```
Acesse a documentação interativa Swagger da API

## Testes
```bash

docker compose exec api python -m run_tests

```
## Encerramento
```bash
docker compose down
```

## Verificando Logs
```bash
docker compose logs -f api
```

## Configuração

As configurações podem ser ajustadas através de variáveis de ambiente:

- `POOL_SIZE`: Número de workers no pool (padrão: 4)
- `WAIT_TIME`: Tempo de espera para elementos na página (padrão: 5)
