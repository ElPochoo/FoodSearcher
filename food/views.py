from django.shortcuts import render
from .models import Food
from django.db.models import Q
import requests
from bs4 import BeautifulSoup
from decimal import Decimal
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
# Create your views here.
def index(request):
    foods = Food.objects.all()
    return render(request, 'index.html', {'foods': foods})

def inf(request):
    query = request.POST.get('query')
    print("query : ", query)


def sup_inf(request):
    if 'inf' in request.POST:
        query = request.POST.get('query')
        foods = Food.objects.filter(price__lt=query)
        return render(request, 'index.html', {'foods': foods})

    else:
        query = request.POST.get('query')
        foods = Food.objects.filter(price__gt=query)
        return render(request, 'index.html', {'foods': foods})

def sortbyprice(request):
    foods = Food.objects.all().order_by('price')
    return render(request, 'index.html', {'foods': foods})

def sortby_price(request):
    foods = Food.objects.all().order_by('-price')
    return render(request, 'index.html', {'foods': foods})

def scrap_baguette(request):

    url = "https://baguettedelivery.tn/"

    # Send a GET request to the URL
    response = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all product containers
    product_containers = soup.find_all("div", class_="prod_hold")

    # Iterate over each product container
    for container in product_containers:
        # Scrape the name
        name_element = container.find("span", class_="name")
        name = name_element.get_text(strip=True)

        # Scrape the price
        price_element = container.find("span", class_="woocommerce-Price-amount")
        
        price = price_element.get_text(strip=True)
        price = price.replace("د.ت", "")
        # Scrape the ingredients
        ingredients_element = container.find("div", class_="woocommerce-product-details__short-description")
        if ingredients_element:
            ingredients = ingredients_element.get_text(strip=True)
        else:
            ingredients = ""     
        

        Food.objects.create(name=name, price=price, ingredients=ingredients, url=url)
        
    foods = Food.objects.all()
    return render(request, 'index.html', {'foods': foods})

def scrap_kfc(request):
    url = "https://kfc.com.tn"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    product_containers = soup.find_all("div", class_="item-inner ajax_block_product col-xs-12 cless")

    for container in product_containers:
        name_element = container.find("h5", class_="product-title")
        name = name_element.get_text(strip=True)

        price_element = container.find("span", class_="price")
        price = price_element.get_text(strip=True)
        price = price.replace("TND", "")
        price = price.replace(",", ".")

        description_element = container.find("div", class_="desc-cate")
        description = description_element.get_text(strip=True)

        Food.objects.create(name=name, price=price, ingredients=description, url=url)

    foods = Food.objects.all()
    return render(request, 'index.html', {'foods': foods})


def scrap_MikeAndBens(request):
    url = "https://mikeandbens.com/index.php/menu/"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    product_containers = soup.find_all("div", class_="elementor-container elementor-column-gap-no")

    for container in product_containers:
        name_element = container.find("h3", class_="elementor-heading-title-size-default")
        name = name_element.get_text(strip=True) if name_element else ""

        description_element = container.find("p", class_="elementor-widget-container")
        description = description_element.get_text(strip=True) if description_element else ""
        
        price_element = container.find("h2", class_="elementor-heading-title-size-default")
        price = price_element.get_text(strip=True) if price_element else ""
        price = price.replace("DT", "")
        price = price.replace("=", "")  
            
        try:
            # Validate the price value
            price = Decimal(price)
        except InvalidOperation:
            # Handle invalid price value
            raise ValidationError('"price" value must be a decimal number.')

    
        
        Food.objects.create(name=name,description=description,price=price, url=url)
    
    foods = Food.objects.all()
    return render(request, 'index.html', {'foods': foods})


def search(request):
    query = request.POST.get('query')
    foods = Food.objects.filter(Q(name__contains=query))
    return render(request, 'index.html', {'foods': foods})

        
