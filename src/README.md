# Web Scraper ABE

This project is a web scraping application built using FastAPI and Selenium, organized according to the ABE (Automation → Builder → Executer) architecture. The application allows users to scrape product data from a specified category on a target website.

## Project Structure

- **automation/**: Contains the FastAPI application and API endpoints.
  - `app.py`: Entry point for the FastAPI application.
  
- **builder/**: Contains the logic for scraping and managing the thread pool.
  - `pool.py`: Manages a pool of persistent threads with Selenium WebDrivers.
  - `scraper.py`: Implements the scraping logic and data parsing.
  
- **executer/**: Acts as a service layer between the API and the scraping pool.
  - `service.py`: Processes API requests and interacts with the scraping pool.
  
- **models/**: Defines data transfer objects (DTOs) for the application.
  - `product.py`: Specifies the structure of product data returned by the API.
  
- **tests/**: Contains integration tests for the application.
  - `test_integration.py`: Tests the scraping endpoint using httpx.AsyncClient.
  
- **requirements.txt**: Lists the dependencies required for the project.

- **Dockerfile**: Defines the Docker image for the application.

- **docker-compose.yml**: (Optional) Facilitates easier management of the Docker container.

- **settings.py**: Contains configuration settings for the application.

## Getting Started

### Prerequisites

- Docker
- Docker Compose (optional)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd webscraper-abe
   ```

2. Build and run the application using Docker:
   ```
   docker compose up --build
   ```

### Usage

Once the application is running, you can access the scraping endpoint:

```
GET http://localhost:8000/scrape?category=<category_name>
```

Replace `<category_name>` with the desired category to scrape.

### Assumptions and Technical Decisions

- The application uses a pool of 4 persistent threads to manage concurrent scraping tasks efficiently.
- Selenium is used for web scraping, with explicit waits implemented to ensure robust scraping without unnecessary delays.
- The API returns product data in JSON format, structured according to the defined DTOs.
- Integration tests are included to verify the functionality of the API endpoint.

### License

This project is licensed under the MIT License.