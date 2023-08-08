import requests
from bs4 import BeautifulSoup
import csv
import time

def get_product_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title = soup.find('span', {'id': 'productTitle'})
    if title:
        title = title.get_text().strip()
    else:
        title = 'N/A'
    
    price = soup.find('span', {'class': 'a-price-whole'})
    if price is None:
        price = soup.find('span', {'id': 'priceblock_dealprice'})
    if price is None:
        price = 'N/A'
    else:
        price = price.get_text().strip()
    
    rating = soup.find('span', {'class': 'a-icon-alt'})
    if rating is None:
        rating = 'N/A'
    else:
        rating = rating.get_text().split()[0]
    
    reviews = soup.find('span', {'id': 'acrCustomerReviewText'})
    if reviews:
        reviews = reviews.get_text().split()[0]
    else:
        reviews = 'N/A'
    
    description = soup.find('div', {'id': 'productDescription'})
    if description:
        description = description.get_text().strip()
    else:
        description = 'N/A'
    
    return {
        'Title': title,
        'Price': price,
        'Rating': rating,
        'Reviews': reviews,
        'Description': description
    }

def main():
    keyword = input("Enter a keyword to search on Amazon: ")
    
    products = []
    
    search_url = f"https://www.amazon.in/s?k={keyword.replace(' ', '+')}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    for result in soup.find_all('div', {'data-asin': True}):
        asin = result['data-asin']
        product_url = f"https://www.amazon.in/dp/{asin}"
        product_data = get_product_data(product_url)
        products.append(product_data)
        
    # Save data to CSV
    with open('amazon_products.csv', 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Title', 'Price', 'Rating', 'Reviews', 'Description']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        writer.writeheader()
        for product in products:
            writer.writerow(product)
    
    print(f"{len(products)} products data saved to amazon_products.csv")

if __name__ == "__main__":
    main()
