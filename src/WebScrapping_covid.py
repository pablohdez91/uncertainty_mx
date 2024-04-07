# Modules
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

# Directory
"""
import os
path = ""
os.chdir(path)
"""

# Search parameters
periodico = "reforma"   # "reforma", "mural" o "elnorte"
busqueda = "economia incertidumbre coronavirus"
fechas_ = pd.date_range('2020-01-01', '2020-05-31', freq='D')
fechas = []
for f in fechas_:
    fechas.append(str(f)[0:10])

url = 'https://busquedas.gruporeforma.com/{}/BusquedasComs.aspx'.format(periodico)

# Start Navigation
# Chromedrive.exe must be in path
driver = webdriver.Chrome() # Chromedrive.exe debe estar en path
driver.get(url)

# Iteration over pages to extract total articles per day
i = 0
I = len(fechas)
hoy = []
while i < I:
    # Search
    driver.find_element_by_name('txtTextSearch').send_keys('hoy')
    driver.find_element_by_name('txtFechaIni').send_keys(fechas[i])
    driver.find_element_by_name('txtFechaFin').send_keys(fechas[i])
    driver.find_element_by_id('imbBuscar').click()

    time.sleep(5)   # For avoid IP blocks

    # Clean Search
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

# Clean Search
driver.find_element_by_name('txtTextSearch').clear()
driver.find_element_by_name('txtFechaIni').clear()
driver.find_element_by_name('txtFechaFin').clear()


# Iteration over pages to extract articles per day with the keywords
covid = []
i = 0
while i < I:
    # Search
    driver.find_element_by_name('txtTextSearch').send_keys(busqueda)
    driver.find_element_by_name('txtFechaIni').send_keys(fechas[i])
    driver.find_element_by_name('txtFechaFin').send_keys(fechas[i])
    driver.find_element_by_id('imbBuscar').click()

    time.sleep(5)   # Avoid IP blocks

    # Clean Search
    driver.find_element_by_name('txtTextSearch').clear()
    driver.find_element_by_name('txtFechaIni').clear()
    driver.find_element_by_name('txtFechaFin').clear()

    # Extract number of articles
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articulos = soup.find('span', class_='totalRegistros').text
    articulos = articulos.replace(",", "")
    articulos = int(articulos)

    covid.append([fechas[i], articulos])
    i += 1

driver.quit()


# Save as csv
df1 = pd.DataFrame(covid)
df2 = pd.DataFrame(hoy)

df1['hoy'] = df2[1]
df1['adj_covid'] = df1[1] / df1['hoy']

df1.to_csv('covid_{}.csv'.format(periodico), index = False)
