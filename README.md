# Amazon Product Scraper

This project is a Django application that integrates Celery to periodically scrape and manage product data for specific Amazon brands. The system allows users to define brands, scrape product information, and manage it through a Django admin interface.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Task Management](#task-management)
- [Anti-Scraping Measures](#anti-scraping-measures)
- [Assumptions and Design Decisions](#assumptions-and-design-decisions)
- [License](#license)

## Features

- Define and manage Amazon brands via the Django Admin interface.
- Scrape product information, including product name, ASIN, SKU, and image URL.
- Automatically update product lists four times a day using Celery tasks.
- Basic REST API to list products by brand.
- Anti-scraping measures implemented to reduce the likelihood of being blocked by Amazon.

## Technologies Used

- **Python**: Programming language used to build the application.
- **Django**: Web framework for building the application.
- **Celery**: Asynchronous task queue for scheduling periodic scraping tasks.
- **Redis**: Message broker for Celery tasks.
- **BeautifulSoup**: Library for web scraping.
- **Requests**: Library for making HTTP requests.
- **Django Rest Framework**: For building RESTful APIs.

## Setup Instructions

### Prerequisites

1. Python 3.x
2. Django
3. Redis
4. Celery

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/asadDev29/amazon-scrapper.git
   cd amazon-scraper
2. **Create a virtual environment**
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. **Install the required packages**
    pip install -r requirements.txt
4. **Set up the database**
    python manage.py makemigrations
    python manage.py migrate
5. **Create a superuser for the Django Admin**
    python manage.py createsuperuser
6. **Run the Django server**
    python manage.py runserver
7. **Start the Celery worker and beat scheduler in separate terminals**
    # Terminal 1: Start Celery worker
    celery -A amazon_scraper worker -l info

    # Terminal 2: Start Celery beat for periodic tasks
    celery -A amazon_scraper beat -l info
### Usage

1. Access the Django Admin: Open http://127.0.0.1:8000/admin/ and log in using the superuser account created.
2. Add Brands: Create entries for the Amazon brands you want to scrape.
3. Run the Scraper: The scraper will automatically run every six hours to update product data.
4. View Products: Check the products associated with each brand in the Django Admin.

### API Endpoints

1. List Brands: GET /api/brands/
2. List Products: GET /api/products/
3. Create Brand: POST /api/brands/
4. Create Product: POST /api/products/
You can use tools like Postman or curl to interact with the API endpoints.

### Task Management
The scraping tasks are managed by Celery and are scheduled to run four times a day. You can manually trigger the task in the Django shell as follows:
python manage.py shell    #in terminal
from products.tasks import update_products
update_products.delay()

### Anti-Scraping Measures
The scraper includes several anti-scraping measures, such as:

1. Randomized user-agent rotation.
2. Random delays between requests to avoid detection.
3. Handling of CAPTCHA and potential blocking.

### Assumptions and Design Decisions

The scraping logic is designed for a specific HTML structure, which may change. Regular updates to the selectors may be necessary.
The application assumes a basic understanding of Django, Python, and web scraping concepts.