
from celery import shared_task
from .scraper import scrape_brand_products
from .models import Brand

@shared_task
def update_products():
    brands = Brand.objects.all()
    for brand in brands:
        scrape_brand_products(brand)
