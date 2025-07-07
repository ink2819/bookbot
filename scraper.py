import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


BASE_URL = "https://3ssstudios.com"
START_URL = f"{BASE_URL}/collections/publications"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

all_items = []

def scrape_detail_page(url):
    try:
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.content, "html.parser")

        # Extract brand
        brand_tag = soup.find("p", itemprop="brand")
        brand = brand_tag.get_text(strip=True) if brand_tag else None

        # Extract description
        desc_tag = soup.find("div", itemprop="description")
        description = desc_tag.get_text(strip=True) if desc_tag else None

        return brand, description
    except Exception as e:
        print(f"Error scraping detail page {url}: {e}")
        return None, None

def scrape_page(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    catalog_container = soup.find("div", class_="grid grid--uniform grid--view-items")
    if not catalog_container:
        return [], None

    items = []

    for item in catalog_container.find_all("div", class_="grid-view-item"):
        img_tag = item.find("img", class_="grid-view-item__image")
        image_link = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None

        title_tag = item.find("div", class_="h4 grid-view-item__title")
        title = title_tag.get_text(strip=True) if title_tag else None

        a_tag = item.find("a", href=True)
        item_url = f"{BASE_URL}{a_tag['href']}" if a_tag else None

       
        brand, description = scrape_detail_page(item_url) if item_url else (None, None)

        items.append({
            "title": title,
            "image link": image_link,
            "url": item_url,
            "brand": brand,
            "description": description
        })

        time.sleep(0.5)  

    next_page = find_next_url(soup)
    return items, next_page

def find_next_url(soup):
    pagination_links = soup.select("a.btn.btn--secondary.btn--narrow")
    for link in pagination_links:
        if ">" in link.get_text() or "Next" in link.get_text():
            return BASE_URL + link['href']
    return None

next_page = START_URL
while next_page:
    print(f"Scraping: {next_page}")
    items, next_page = scrape_page(next_page)
    all_items.extend(items)
    time.sleep(1)

dfBungee = pd.DataFrame(all_items)





driver_path = r"C:/Users/aliso/Downloads/chromedriver-win64/chromedriver.exe"


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")


service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

all_books = []


for page in range(1, 6):  
    url = f"https://centerforbookarts.org/book-shop?cats=artists-books&pg={page}"
    print(f"Scraping: {url}")
    
    driver.get(url)
    time.sleep(2)  

    soup = BeautifulSoup(driver.page_source, "html.parser")
    posts = soup.find_all('div', class_='post-content')

    for post in posts:
        category_div = post.find('div', class_='post-header')
        category = category_div.get_text(strip=True) if category_div else None

        title_tag = post.find('h2', class_='post-title')
        title = title_tag.get_text(strip=True) if title_tag else None

        image_div = post.find('div', class_='post-image')
        img_tag = image_div.find('img', decoding='async') if image_div else None
        image_link = img_tag['src'] if img_tag else None

        a_tag = post.find('a') if post else None
        book_url = a_tag['href'] if a_tag and 'href' in a_tag.attrs else None
        book_url = book_url if book_url.startswith('http') else f"https://centerforbookarts.org{book_url}"

 
        brand = None
        description = None


        if book_url:
            try:
                driver.get(book_url)
                time.sleep(1.5)  

                detail_soup = BeautifulSoup(driver.page_source, "html.parser")

                brand_tag = detail_soup.find('h2', class_='hero-subtitle')
                brand = brand_tag.get_text(strip=True) if brand_tag else None

                col_div = detail_soup.find('div', class_='col')
                if col_div:
                    p_tag = col_div.find('p')
                    description = p_tag.get_text(strip=True) if p_tag else None

            except Exception as e:
                print(f"Error scraping detail page {book_url}: {e}")

        all_books.append({
            'title': title,
            'image link': image_link,
            'url': item_url,
            'brand': brand,
            'description': description
        })

driver.quit()

dfCBA = pd.DataFrame(all_books)


df_combined = pd.concat([dfCBA, dfBungee], ignore_index=True)
df_combined.to_csv("output.csv", index=False)