"""
- Este código accede a cualquiera de los buscadores de los periodicos de Grupo
    Reforma (Reforma, Mural o El Norte) y hace Web Scrapping de los artículos 
    periodisticos encontrados despues de una busqueda.

- El output del código es el archivo noticias.db, contiene las variables:
    fecha, titulo y articulo.

- Es necesaria una conexion "directa" al periodico, es decir, que se pueda 
    acceder directamente a las noticias sin necesidad de registrarse.
"""


# Modulos
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
from math import ceil
import sqlite3

"""
import os
path = ""
os.chdir(path)
"""


# definicion de funciones SQLite
# Importante agregar el nombre del periodico
Periodico = 'Reforma'
def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS {}(fecha TEXT, titulo TEXT, articulo TEXT)".format(Periodico))

def insert_data():
    for i in range(len(links)):
        f = fechas[i]
        t = titulos[i]
        a = articulos[i]
        
        c.execute("INSERT INTO {}(fecha, titulo, articulo) VALUES(?, ?, ?)".format(Periodico), 
                  (f, t, a))
        conn.commit()



# Importante Revisar parámetros de búsqueda antes de ejecutar
busqueda = "economia incertidumbre"
fecha_ini = '01-01-2020'    # formato: dd-mm-yyyy
fecha_fin = '31-03-2020'    # formato: dd-mm-yyyy

periodico = 'reforma' # 'reforma', 'mural' o 'elnorte'



# Inicio
url = 'https://busquedas.gruporeforma.com/{}/BusquedasComs.aspx'.format(periodico)
base = 'https://busquedas.gruporeforma.com/{}/'.format(periodico)
chrome = "C:\\Users\\Pablo\\chromedriver.exe"
noticias = 'noticias.db'

driver = webdriver.Chrome(chrome)
driver.get(url)


# Introduce parámetros de búsqueda:
driver.find_element_by_name('txtTextSearch').send_keys(busqueda)
driver.find_element_by_name('txtFechaIni').send_keys(fecha_ini)
driver.find_element_by_name('txtFechaFin').send_keys(fecha_fin)
driver.find_element_by_id('rb_orden_2').click() 

#### Wait para que cargue la página
time.sleep(5)

#### Definimos el numero total de paginas
soup = BeautifulSoup(driver.page_source, 'html.parser')
P = soup.find('span', class_='totalRegistros').text
P = P.replace(",", "")
P = int(P)
P = ceil(P/20)  # 20 es el número de articulos por página
del soup


# abre conección a la base
conn = sqlite3.connect(noticias)
c = conn.cursor()
create_table()


t_inicial = time.time()
### Comenzamos a iterar
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
    
    ### recoge los contenidos de las noticias por link
    articulos = []
    for l in range(len(links)):
        r = requests.get(base+links[l])
        soup_texto = BeautifulSoup(r.text, 'html.parser')
        art = str(soup_texto.find('div', class_='Scroll').find_all('div', class_='texto'))
        articulos.append(art)    

    #### Agrega las cosas a la base
    insert_data()
    
    #### Cambia la pagina
    pag += 1
    if pag <= P:
        driver.find_element_by_id('a_pagina_' + str(pag)).click()
        t_avance = time.time()
        print('Progreso: pagina ' + str(pag) + " ... " + str(t_avance-t_inicial)+' Segundos')
        time.sleep(5) # Espera para evitar bloqueos de IP 
### Fin de la Iteración

driver.quit()

### Cierra conección a la base
c.close
conn.close()


print('.................. Done!')