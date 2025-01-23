from main import fetch_data
import requests
from bs4 import BeautifulSoup
import mysql.connector  
import time
# from contextlib import closing  





DB_HOST = 'localhost'  
DB_USER = '****'  
DB_PASS = '****'  
DB_NAME = 'bayut_db'  

# All other imports and fetch_data function remain the same  

def insert_data(data):  
    try:  
        connection = mysql.connector.connect(  
            host=DB_HOST,  
            user=DB_USER,  
            password=DB_PASS,  
            database=DB_NAME
        )  
        
        if connection.is_connected():  
            cursor = connection.cursor()  
            for item in data:  
                cursor.execute("""  
                    INSERT INTO properties (price, property_type, purpose, size, region, trucheck)  
                    VALUES (%s, %s, %s, %s, %s, %s);  
                """, (item['price'], item['type'], item['purpose'], item['size'], item['region'], item['trucheck'] if item['trucheck'] else 'false'))  
            connection.commit()  
    except Exception as e:  
        print(f"Error: {e}")  
    finally:  
        if connection.is_connected():  
            cursor.close()  
            connection.close()



def get_info():
    links = fetch_data()
    data = []
    for link in links:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")
        price = soup.find('span', {'aria-label': 'Price'}).text.strip()
        type_ = soup.find('span', {'aria-label': 'Type'}).text.strip()
        purpose = soup.find('span', {'aria-label': 'Purpose'}).text.strip()

        size = soup.find('span', {'aria-label': 'Area'}).text.strip()
        region = soup.find('div', {'aria-label': 'Property header'}).text.strip().split(',')[-2]
        trucheck_element = soup.find('span', {'aria-label': 'Trucheck date'})
        trucheck = trucheck_element.text.strip() if trucheck_element else None
        data.append({
            "price": price,
            "type": type_,
            "purpose": purpose,
            "size": size,
            "region": region,
            "trucheck": trucheck
        })
    
    insert_data(data)
    print(data)
    return data


def crawl_new_listings(period=60):
    """Continuously crawls new property listings."""
    fetched_links = set()

    while True:
        print("Fetching new listings...")
        new_links = fetch_data()

        for link in new_links:
            if link not in fetched_links:
                print(f"New listing found: {link}")
                fetched_links.add(link)
                property_data = get_info(link)
                if property_data:
                    insert_data([property_data])

        print(f"Sleeping for {period} seconds before the next fetch...")
        time.sleep(period)

if __name__ == "__main__":
    crawl_new_listings(period=300) 
    get_info()