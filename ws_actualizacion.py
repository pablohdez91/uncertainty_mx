# Modulos
from selenium import webdriver
from bs4 import BeautifulSoup
# import requests
import time
from math import ceil
import sqlite3

# definicion de funciones SQLite
def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS Elnorte(fecha TEXT, titulo TEXT, articulo TEXT)")

def insert_data():
    for i in range(len(links)):
        f = fechas[i]
        t = titulos[i]
        a = articulos[i]
        
        c.execute("INSERT INTO Elnorte(fecha, titulo, articulo) VALUES(?, ?, ?)", 
                  (f, t, a))
        conn.commit()

# Directorios
import os
path = "C:/Users/Pablo/Documents/MAESTRIA/TESIS/programas"
os.chdir(path)


# Inicio
url = 'https://busquedas.gruporeforma.com/elnorte/BusquedasComs.aspx'
base = 'https://busquedas.gruporeforma.com/elnorte/'
chrome = "C:\\Users\\Pablo\\chromedriver.exe"

# parametros de búsqueda
busqueda = "economia incertidumbre"
fecha_ini = '01-05-2020'
fecha_fin = '31-05-2020'


# inicia navegacion ---------------------------------------------------------
driver = webdriver.Chrome()
driver.get('https://elnorte.com')

##### Aqui se introduce usuario y contraseña manualmente antes de seguir #####
driver.get(url)

# Introduce parámetros de búsqueda:
driver.find_element_by_name('txtTextSearch').send_keys(busqueda)
driver.find_element_by_name('txtFechaIni').send_keys(fecha_ini)
driver.find_element_by_name('txtFechaFin').send_keys(fecha_fin)
driver.find_element_by_id('rb_orden_2').click() # con este ya hace la busqueda

#### Wait para que cargue la página
time.sleep(5)

#### Definimos parámetros del ciclo
soup = BeautifulSoup(driver.page_source, 'html.parser')
P = soup.find('span', class_='totalRegistros').text
P = P.replace(",", "")
P = int(P)
P = ceil(P/20)  #20 es el número de articulos por página
pag = 1
#P = 5
del soup

t_inicial = time.time()
### Primera iteración

fechas = []; titulos = []; links = []
while pag <= P:
    ### parsea la página
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    ### recoge fechas
    soup_fechas = soup.find_all('p', class_='fecha')
    for i in range(len(soup_fechas)):
        fechas.append(soup_fechas[i].text)
    
    ### recoge titulos
    soup_titulos = soup.find_all('a', class_='hoverC')
    
    for i in range(len(soup_titulos)):
        titulos.append(soup_titulos[i].text)
        
    ### recoge links a las notas
    for i in range(len(soup_titulos)):
        links.append(soup_titulos[i]['href'])
    
    #### Cambia la hoja
    pag = pag + 1
    if pag <= P:
        driver.find_element_by_id('a_pagina_' + str(pag)).click()
        #t_avance = time.time()
        #print('pasamos a pagina ' + str(pag) + " ... " + str(t_avance-t_inicial)+' Segundos')
        time.sleep(15) # Espera para evitar bloqueos de IP 
### Fin de la Iteración        
        
        
### Segunda Iteración
articulos = []
for l in range(len(links)):
    driver.get(base+links[l])
    soup_texto = BeautifulSoup(driver.page_source, 'html.parser')
    art = str(soup_texto.find('div', class_='Scroll').find_all('div', class_='texto'))
    articulos.append(art) 
    time.sleep(5)

# driver.quit()

print('.................. Done!')

# abre conección a la base
conn = sqlite3.connect('noticias_ene20-abr20.db')
c = conn.cursor()
# create_table()

#### Agrega las cosas a la base
insert_data()

### Cierra conección a la base
c.close
conn.close()




