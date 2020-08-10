# Modulos
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from math import ceil
import sqlite3


# Definicion de funciones SQLite
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


"""
import os
path = ""
os.chdir(path)
"""


# parametros de búsqueda
busqueda = "economia incertidumbre"
fecha_ini = '01-06-2020'
fecha_fin = '30-06-2020'


# Inicio
url = 'https://busquedas.gruporeforma.com/{}/BusquedasComs.aspx'.format(periodico)
base = 'https://busquedas.gruporeforma.com/{}/'.format(periodico)
chrome = "C:\\Users\\Pablo\\chromedriver.exe"
noticias = 'Corpus.db'


# inicia navegacion ---------------------------------------------------------
# Instertar Usuario y contraseña
driver_art = webdriver.Chrome()
driver_art.get('https://{}.com'.format(periodico))

driver = webdriver.Chrome()
driver.get(url)


# Introduce parámetros de búsqueda:
driver.find_element_by_name('txtTextSearch').send_keys(busqueda)
driver.find_element_by_name('txtFechaIni').send_keys(fecha_ini)
driver.find_element_by_name('txtFechaFin').send_keys(fecha_fin)
driver.find_element_by_id('rb_orden_2').click()

#### Wait para que cargue la página
time.sleep(5)

#### Numero total de paginas
soup = BeautifulSoup(driver.page_source, 'html.parser')
P = soup.find('span', class_='totalRegistros').text
P = P.replace(",", "")
P = int(P)
P = ceil(P/20)  # 20 es el número de articulos por página
del soup

# Abre conección a la base
conn = sqlite3.connect(noticias)
c = conn.cursor()
create_table()

t_inicial = time.time()
pag = 1
while pag <= P:
    ### parsea la página
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    ### recoge fechas
    soup_fechas = soup.find_all('p', class_='fecha')
    fechas = []
    for i in range(len(soup_fechas)):
        fechas.append(soup_fechas[i].text)

    ### recoge titulos
    soup_titulos = soup.find_all('a', class_='hoverC')
    titulos = []
    for i in range(len(soup_titulos)):
        titulos.append(soup_titulos[i].text)

    ### recoge links a las notas
    links = []
    for i in range(len(soup_titulos)):
        links.append(soup_titulos[i]['href'])

    ### recoge los artículos completos
    articulos = []
    for l in range(len(links)):
        driver_art.get(base+links[l])
        soup_texto = BeautifulSoup(driver_art.page_source, 'html.parser')
        art = str(soup_texto.find('div', class_='Scroll').find_all('div', class_='texto'))
        articulos.append(art)
        time.sleep(5)

    insert_data()

    #### Cambia la hoja
    pag += 1
    if pag <= P:
        driver.find_element_by_id('a_pagina_' + str(pag)).click()
        t_avance = time.time()
        print('Progreso: pagina ' + str(pag) + " ... " + str(t_avance-t_inicial)+' Segundos')
        time.sleep(5) # Espera para evitar bloqueos de IP

### Fin de la Iteración
driver.quit()
driver_art.quit()

### Cierra conección a la base
c.close
conn.close()

print('.................. Done!')
