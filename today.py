# Modulos
from selenium import webdriver
from bs4 import BeautifulSoup
import time

"""
para cambiar de periodico hay que modificar:
    - url
    - today_reforma
    - today_reforma.append()
    - myFile csv
"""


import os
path = "D:/Tesis/programas/prueba/ws"
os.chdir(path)


# parametros de búsqueda
busqueda = "hoy"
years = list(range(1990, 2021))
dia_fin = ['31', '28', '31', '30', '31', '30', '31', '31', '30', '31', '30', '31']
meses = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
ini = []    # fechas de incio de busqueda
for y in years:
    for m in meses:
        ini.append(str('01'+'-'+m+'-'+str(y)))
        
fin = []    # fechas de final de busqueda
for y in years:
    for i in range(12):
        fin.append(str(dia_fin[i] + '-' + meses[i] + '-' + str(y)))



# ---------------------------------------------------------------------------
#       Reforma
# ---------------------------------------------------------------------------

url = 'https://busquedas.gruporeforma.com/reforma/BusquedasComs.aspx'
# chrome = "C:\\Users\\Pablo\\chromedriver.exe"


# inicia navegacion
driver = webdriver.Chrome()
driver.get(url)


today_reforma = []
for i in range(361):  #hasta Feb 2020
    
    # Busqueda
    driver.find_element_by_name('txtTextSearch').send_keys(busqueda)
    driver.find_element_by_name('txtFechaIni').send_keys(ini[i])
    driver.find_element_by_name('txtFechaFin').send_keys(fin[i])
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

    today_reforma.append([ini[i], articulos])


print('.................. Done!')

driver.quit()

# Guardar como csv
import csv
myFile = open('D:/Tesis/inputs/today_reforma.csv', 'w', newline='')

with myFile as csvfile:
    writer = csv.writer(myFile)
    writer.writerow(['date', 'today'])
    writer.writerows(today_reforma)
    






# ---------------------------------------------------------------------------
#       Mural
# ---------------------------------------------------------------------------

url = 'https://busquedas.gruporeforma.com/mural/BusquedasComs.aspx'


# inicia navegacion
driver = webdriver.Chrome()
driver.get(url)


today_mural = []
for i in range(361):  #hasta Feb 2020
    
    # Busqueda
    driver.find_element_by_name('txtTextSearch').send_keys(busqueda)
    driver.find_element_by_name('txtFechaIni').send_keys(ini[i])
    driver.find_element_by_name('txtFechaFin').send_keys(fin[i])
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

    today_mural.append([ini[i], articulos])


print('.................. Done!')

driver.quit()


# Guardar como csv
import csv
myFile = open('D:/Tesis/inputs/today_mural.csv', 'w', newline='')

with myFile as csvfile:
    writer = csv.writer(myFile)
    writer.writerow(['date', 'today'])
    writer.writerows(today_mural)
    






# ---------------------------------------------------------------------------
#       El Norte
# ---------------------------------------------------------------------------

url = 'https://busquedas.gruporeforma.com/elnorte/BusquedasComs.aspx'


# inicia navegacion
driver = webdriver.Chrome()
driver.get(url)


today_elnorte = []
for i in range(361):  #hasta Feb 2020
    
    # Busqueda
    driver.find_element_by_name('txtTextSearch').send_keys(busqueda)
    driver.find_element_by_name('txtFechaIni').send_keys(ini[i])
    driver.find_element_by_name('txtFechaFin').send_keys(fin[i])
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

    today_elnorte.append([ini[i], articulos])


print('.................. Done!')


# Guardar como csv
import csv
myFile = open('D:/Tesis/inputs/today_elnorte.csv', 'w', newline='')

with myFile as csvfile:
    writer = csv.writer(myFile)
    writer.writerow(['date', 'today'])
    writer.writerows(today_elnorte)
    
