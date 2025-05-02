📖 This README is also available in [Português](./README.pt.md)

# Concurrent Scraper API

Concurrent web scraping API built with FastAPI and Selenium to efficiently extract product data from websites.

## Basic Commands

### Run the API

```bash

docker compose up -d --build

```

### Example Commands
```bash

curl -s 'http://localhost:8000/scrape'
curl -s 'http://localhost:8000/scrape?category=Electronics'

```

### Endpoints

#### Product Scraping

**All products:**
```
GET /scrape
```

**Products from a specific category:**
```
GET /scrape?category=electronics
```

Available categories:
- Apparel
- Cosmetics
- Electronics
- Home Goods

#### API Documentation

```
GET /docs
```
Access the API's interactive Swagger documentation.

## Tests
```bash

docker compose exec api python -m run_tests

```
## Shutdown
```bash
docker compose down
```
## Configuration

Settings can be adjusted through environment variables:

- `POOL_SIZE`: Number of workers in the pool (default: 4)
- `WAIT_TIME`: Wait time for elements on the page (default: 5)
