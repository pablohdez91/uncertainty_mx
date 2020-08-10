# Modulos
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

"""
import os
path = ""
os.chdir(path)
"""

# parametros de búsqueda
fechas_ = pd.date_range('2020-01-01', '2020-05-31', freq='D')
fechas = []
for f in fechas_:
    fechas.append(str(f)[0:10])

busqueda = "economia incertidumbre coronavirus"
periodico = "reforma"   # "reforma", "mural" o "elnorte"

url = 'https://busquedas.gruporeforma.com/{}/BusquedasComs.aspx'.format(periodico)

# inicia navegacion
driver = webdriver.Chrome() # Chromedrive.exe debe estar en path
driver.get(url)

i = 0
I = len(fechas)
hoy = []
while i < I:
    # Busqueda
    driver.find_element_by_name('txtTextSearch').send_keys('hoy')
    driver.find_element_by_name('txtFechaIni').send_keys(fechas[i])
    driver.find_element_by_name('txtFechaFin').send_keys(fechas[i])
    driver.find_element_by_id('imbBuscar').click()

    time.sleep(5)   # evita bloqueos de IP

    # Limpia busqueda
    driver.find_element_by_name('txtTextSearch').clear()
    driver.find_element_by_name('txtFechaIni').clear()
    driver.find_element_by_name('txtFechaFin').clear()

    # Extrae el total de articulos
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articulos = soup.find('span', class_='totalRegistros').text
    articulos = articulos.replace(",", "")
    articulos = int(articulos)

    hoy.append([fechas[i], articulos])
    i = i+1

driver.find_element_by_name('txtTextSearch').clear()
driver.find_element_by_name('txtFechaIni').clear()
driver.find_element_by_name('txtFechaFin').clear()


covid = []
i = 0
while i < I:  #hasta Feb 2020

    # Busqueda
    driver.find_element_by_name('txtTextSearch').send_keys(busqueda)
    driver.find_element_by_name('txtFechaIni').send_keys(fechas[i])
    driver.find_element_by_name('txtFechaFin').send_keys(fechas[i])
    driver.find_element_by_id('imbBuscar').click()

    time.sleep(5)   # evita bloqueos de IP

    # Limpia busqueda
    driver.find_element_by_name('txtTextSearch').clear()
    driver.find_element_by_name('txtFechaIni').clear()
    driver.find_element_by_name('txtFechaFin').clear()

    # Extrae el total de articulos
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articulos = soup.find('span', class_='totalRegistros').text
    articulos = articulos.replace(",", "")
    articulos = int(articulos)

    covid.append([fechas[i], articulos])
    i += 1

driver.quit()


# Guardar como csv
df1 = pd.DataFrame(covid)
df2 = pd.DataFrame(hoy)

df1['hoy'] = df2[1]
df1['adj_covid'] = df1[1] / df1['hoy']

df1.to_csv('covid_{}.csv'.format(periodico), index = False)
