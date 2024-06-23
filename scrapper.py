import requests
from bs4 import BeautifulSoup
# import pandas as pd
import os
# import csv

# Function to scrape product data from a category page


def scrape_category(url, cookies):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    page_number = 1
    product_links = []

    while True:
        page_url = f"{url}&p={page_number}&product_list_limit=36"
        response = requests.get(page_url, headers=headers, cookies=cookies)

        if response.status_code != 200:
            print(
                f"Failed to retrieve page {page_number}. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        # the type3 string is specific to ennovamarket
        products = soup.find_all('div', class_='product-item-info type3')

        if not products:
            print(f"No more products found on page {page_number}. Exiting.")
            break

        for product in products:
            product_link = product.find('a')['href']
            product_links.append(product_link)

        page_number += 1

    return product_links

# Function to scrape product details from individual product pages


def scrape_product(url, cookies):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    # temprarly take the cookies out
    # response = requests.get(url, headers=headers, cookies=cookies)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract product details (modify based on actual HTML structure)
        title = soup.find('h1', class_='page-title').text.strip()
        description = soup.find(
            'div', class_='product attribute description').text.strip()
        price = soup.find('span', class_='price').text.strip()
        image_url = soup.find('img', class_='fotorama__img')['src']

        # Download image
        # assuming image URL ends with .jpg
        image_filename = url.split('/')[-1] + '.jpg'
        image_path = os.path.join('data', 'images', image_filename)
        with open(image_path, 'wb') as img_file:
            img_data = requests.get(image_url).content
            img_file.write(img_data)

        return {
            'Title': title,
            'Description': description,
            'Price': price,
            'Image URL': image_url,
            'Image Path': image_path
        }
    else:
        print(
            f"Failed to retrieve product page {url}. Status code: {response.status_code}")
        return None

# Main function to orchestrate scraping process


def main():
    base_url = 'https://ennovamarket.ma/grandstream.html?_=1719174970150'
    cookies = {
        # Replace with your actual cookies after logging in
        'cookie_name': 'cookie_value'
    }

    product_links = scrape_category(base_url, cookies)

    # Save product links to a file
    links_path = os.path.join('data', 'product_links.txt')
    with open(links_path, 'w') as file:
        for link in product_links:
            file.write(f"{link}\n")
    print(f"Product links saved to {links_path}")

    # scraped_data = []
    # for link in product_links:
    #     product_data = scrape_product(link, cookies)
    #     if product_data:
    #         scraped_data.append(product_data)
    #
    # # Save data to CSV
    # df = pd.DataFrame(scraped_data)
    # csv_path = os.path.join('data', 'products.csv')
    # df.to_csv(csv_path, index=False, quoting=csv.QUOTE_NONNUMERIC)
    # print(f"Scraped data saved to {csv_path}")


if __name__ == "__main__":
    main()
