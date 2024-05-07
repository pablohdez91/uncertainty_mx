from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from bs4 import BeautifulSoup
import time
from math import ceil

from pymongo.mongo_client import MongoClient


load_dotenv()
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def db_connection():
    uri = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@cluster0.k2mhzdx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0".format(DB_USERNAME, DB_PASSWORD)

    # Create a new client and connect to the server
    client = MongoClient(uri)

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    
    return client


def insert_base_parameters():
    driver.find_element(By.ID, 'txtTextSearch').send_keys('economia incertidumbre')
    driver.find_element(By.NAME, 'txtFechaIni').send_keys(fecha_ini)
    driver.find_element(By.NAME, 'txtFechaFin').send_keys(fecha_fin)
    driver.find_element(By.ID, 'rb_orden_2').click()
    time.sleep(5)


def define_iterations(soup):
    P = soup.find('span', class_='totalRegistros').text
    P = P.replace(",", "")
    P = int(P)
    P = ceil(P/20)  # 20 es el número de articulos máximo por página
    return P


def remove_tags(soup):
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
 
    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)


def get_article(link):
    driver_art.get(link)
    time.sleep(5)

    soup_article = BeautifulSoup(driver_art.page_source, 'html.parser')
    article = remove_tags(soup_article)
    return article


def get_data(soup):
    soup_headers = soup.find_all('tr')

    data = []
    for i in range(len(soup_headers)):
        try:
            fecha = soup_headers[i].find('p', class_='fecha').text
            link = base + soup_headers[i].find('a')['href']
            titulo = soup_headers[i].find('a', class_='hoverC').text
            articulo = get_article(link)

            document = {
                'fecha': fecha,
                'titulo': titulo,
                'link': link,
                'periodico': periodico,
                'articulo': articulo
            }

            data.append(document)
        except:
            pass
        
    return data


def change_page(pag, P):
    if pag <= P:
        driver.find_element(By.ID, 'a_pagina_' + str(pag)).click()
        time.sleep(5) # Wait for avoid IP blocks


client = db_connection()

db = client.Corpusdb
coll = db.Corpus


periodico = 'reforma' # reforma, elnorte, mural
busqueda = "economia incertidumbre"
fecha_ini = '01-01-1993'
fecha_fin = '31-12-1993'
url = 'https://busquedas.gruporeforma.com/{}/BusquedasComs.aspx'.format(periodico)
base = 'https://busquedas.gruporeforma.com/{}/'.format(periodico)

# Start Navigation
# In driver_art it is necessary to insert username and password manually on the page
# Chromedrive.exe must be in path
driver_art = webdriver.Chrome()
driver = webdriver.Chrome()
driver_art.get('https://{}.com'.format(periodico))
driver.get(url)


insert_base_parameters()
soup = BeautifulSoup(driver.page_source, 'html.parser')
P = define_iterations(soup)
pag = 1

while pag <= P:
    pag += 1
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    data = get_data(soup)
    coll.insert_many(data)
    change_page(pag, P)