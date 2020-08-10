# Modules
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from math import ceil
import sqlite3

# Directory
"""
import os
path = ""
os.chdir(path)
"""

# SQLite Functions
periodico = 'Reforma'    # "Reforma", "Mural" o "Elnorte"
def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS {}(fecha TEXT, titulo TEXT, articulo TEXT)".format(periodico))

def insert_data():
    for i in range(len(links)):
        f = fechas[i]
        t = titulos[i]
        a = articulos[i]

        c.execute("INSERT INTO {}(fecha, titulo, articulo) VALUES(?, ?, ?)".format(periodico),
                  (f, t, a))
        conn.commit()


# Search Parameters
busqueda = "economia incertidumbre"
fecha_ini = '01-06-2020'
fecha_fin = '30-06-2020'
url = 'https://busquedas.gruporeforma.com/{}/BusquedasComs.aspx'.format(periodico)
base = 'https://busquedas.gruporeforma.com/{}/'.format(periodico)
Corpus = 'data/Corpus.db'


# Start Navigation
# In driver_art it is necessary to insert username and password manually on the page
# Chromedrive.exe must be in path
driver_art = webdriver.Chrome()
driver = webdriver.Chrome()
driver_art.get('https://{}.com'.format(periodico))
driver.get(url)

# Insert search parameters in the page
driver.find_element_by_name('txtTextSearch').send_keys(busqueda)
driver.find_element_by_name('txtFechaIni').send_keys(fecha_ini)
driver.find_element_by_name('txtFechaFin').send_keys(fecha_fin)
driver.find_element_by_id('rb_orden_2').click()
time.sleep(5)

# Get total number of pages for iteration
soup = BeautifulSoup(driver.page_source, 'html.parser')
P = soup.find('span', class_='totalRegistros').text
P = P.replace(",", "")
P = int(P)
P = ceil(P/20)  # 20 es el número de articulos por página
del soup

# Connect with the SQL database
conn = sqlite3.connect(Corpus)
c = conn.cursor()
create_table()

# Iteration over pages
t_inicial = time.time()
pag = 1
while pag <= P:
    ### parse the page
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    ### scrapping dates
    soup_fechas = soup.find_all('p', class_='fecha')
    fechas = []
    for i in range(len(soup_fechas)):
        fechas.append(soup_fechas[i].text)

    ### scrapping titles
    soup_titulos = soup.find_all('a', class_='hoverC')
    titulos = []
    for i in range(len(soup_titulos)):
        titulos.append(soup_titulos[i].text)

    ### scrapping links
    links = []
    for i in range(len(soup_titulos)):
        links.append(soup_titulos[i]['href'])

    ### scrapping articles
    articulos = []
    for l in range(len(links)):
        driver_art.get(base+links[l])
        soup_texto = BeautifulSoup(driver_art.page_source, 'html.parser')
        art = str(soup_texto.find('div', class_='Scroll').find_all('div', class_='texto'))
        articulos.append(art)
        time.sleep(5)

    insert_data()

    #### Change the page
    pag += 1
    if pag <= P:
        driver.find_element_by_id('a_pagina_' + str(pag)).click()
        t_avance = time.time()
        print('Progress: page ' + str(pag) + " ... " + str(t_avance-t_inicial)+' Seconds')
        time.sleep(5) # Wait for avoid IP blocks

### Close drivers and database connection
driver.quit()
driver_art.quit()

c.close
conn.close()

print('.................. Done!')
