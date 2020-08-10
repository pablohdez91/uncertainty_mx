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
periodico = 'reforma'  # "reforma", "mural" o "elnorte"
busqueda = 'hoy'
fechas = pd.date_range('1990-01-01', '2020-06-01', freq='M')
fecha_ini = []; fecha_fin = []
for f in fechas:
    fecha_ini.append(str(f)[0:8] + '01')
    fecha_fin.append(str(f)[0:10])

url = 'https://busquedas.gruporeforma.com/{}/BusquedasComs.aspx'.format(periodico)


# Sart Navigation
# Chromedrive.exe must be in path
driver = webdriver.Chrome()
driver.get(url)

today = []
for i in range(len(fecha_ini)):

    # Search
    driver.find_element_by_name('txtTextSearch').send_keys(busqueda)
    driver.find_element_by_name('txtFechaIni').send_keys(fecha_ini[i])
    driver.find_element_by_name('txtFechaFin').send_keys(fecha_fin[i])
    driver.find_element_by_id('imbBuscar').click()

    time.sleep(5)   # Avoid IP blocks

    # Clean Search
    driver.find_element_by_name('txtTextSearch').clear()
    driver.find_element_by_name('txtFechaIni').clear()
    driver.find_element_by_name('txtFechaFin').clear()

    # Scrapping number of articles
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articulos = soup.find('span', class_='totalRegistros').text
    articulos = articulos.replace(",", "")
    articulos = int(articulos)

    today.append([fecha_ini[i], articulos])

driver.quit()

print('.................. Done!')

# Save as csv
import csv
myFile = open('data/today_{}.csv'.format(periodico), 'w', newline='')

with myFile as csvfile:
    writer = csv.writer(myFile)
    writer.writerow(['date', 'today'])
    writer.writerows(today)
