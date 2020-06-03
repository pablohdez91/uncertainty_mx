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
path = "C:/Users/Pablo/Documents/MAESTRIA/TESIS/programas"
os.chdir(path)

# parametros de búsqueda
busqueda = "economia incertidumbre coronavirus"
fechas = ['01-01-2020', '02-01-2020', '03-01-2020', '04-01-2020', '05-01-2020',
'06-01-2020', '07-01-2020', '08-01-2020', '09-01-2020', '10-01-2020', '11-01-2020',
'12-01-2020', '13-01-2020', '14-01-2020', '15-01-2020', '16-01-2020', '17-01-2020',
'18-01-2020', '19-01-2020', '20-01-2020', '21-01-2020', '22-01-2020', '23-01-2020',
'24-01-2020', '25-01-2020', '26-01-2020', '27-01-2020', '28-01-2020', '29-01-2020',
'30-01-2020', '31-01-2020', '01-02-2020', '02-02-2020', '03-02-2020', '04-02-2020',
'05-02-2020', '06-02-2020', '07-02-2020', '08-02-2020', '09-02-2020', '10-02-2020',
'11-02-2020', '12-02-2020', '13-02-2020', '14-02-2020', '15-02-2020', '16-02-2020',
'17-02-2020', '18-02-2020', '19-02-2020', '20-02-2020', '21-02-2020', '22-02-2020',
'23-02-2020', '24-02-2020', '25-02-2020', '26-02-2020', '27-02-2020', '28-02-2020',
'29-02-2020', '01-03-2020', '02-03-2020', '03-03-2020', '04-03-2020', '05-03-2020',
'06-03-2020', '07-03-2020', '08-03-2020', '09-03-2020', '10-03-2020', '11-03-2020',
'12-03-2020', '13-03-2020', '14-03-2020', '15-03-2020', '16-03-2020', '17-03-2020',
'18-03-2020', '19-03-2020', '20-03-2020', '21-03-2020', '22-03-2020', '23-03-2020',
'24-03-2020', '25-03-2020', '26-03-2020', '27-03-2020', '28-03-2020', '29-03-2020',
'30-03-2020', '31-03-2020', '01-04-2020', '02-04-2020', '03-04-2020', '04-04-2020',
'05-04-2020', '06-04-2020', '07-04-2020', '08-04-2020', '09-04-2020', '10-04-2020',
'11-04-2020', '12-04-2020', '13-04-2020', '14-04-2020', '15-04-2020', '16-04-2020',
'17-04-2020', '18-04-2020', '19-04-2020', '20-04-2020', '21-04-2020', '22-04-2020',
'23-04-2020', '24-04-2020', '25-04-2020', '26-04-2020', '27-04-2020', '28-04-2020',
'29-04-2020', '30-04-2020', '01-05-2020', '02-05-2020', '03-05-2020', '04-05-2020',
'05-05-2020', '06-05-2020', '07-05-2020', '08-05-2020', '09-05-2020', '10-05-2020',
'11-05-2020', '12-05-2020', '13-05-2020', '14-05-2020', '15-05-2020', '16-05-2020',
'17-05-2020', '18-05-2020', '19-05-2020', '20-05-2020', '21-05-2020', '22-05-2020',
'23-05-2020', '24-05-2020', '25-05-2020', '26-05-2020', '27-05-2020', '28-05-2020',
'29-05-2020']
I = len(fechas)

# ---------------------------------------------------------------------------
#       Reforma
# ---------------------------------------------------------------------------

url = 'https://busquedas.gruporeforma.com/reforma/BusquedasComs.aspx'

# inicia navegacion
driver = webdriver.Chrome() # Chromedrive.exe debe estar en path
driver.get(url)

hoy = []
i = 0
while i < I:  #hasta Feb 2020
    
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
    i = i + 1

driver.quit()


# Guardar como csv
import pandas as pd
df1 = pd.DataFrame(covid)
df2 = pd.DataFrame(hoy)

df1['hoy'] = df2[1]
df1['adj_covid'] = df1[1] / df1['hoy']

df1.to_csv('covid_reforma.csv', index = False)






# ---------------------------------------------------------------------------
#       Mural
# ---------------------------------------------------------------------------

url = 'https://busquedas.gruporeforma.com/mural/BusquedasComs.aspx'

# inicia navegacion
driver = webdriver.Chrome() # Chromedrive.exe debe estar en path
driver.get(url)

hoy = [] ; covid = []
i = 0
while i < I:  #hasta Feb 2020
    
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
    i = i + 1

driver.quit()


# Guardar como csv
import pandas as pd
df1 = pd.DataFrame(covid)
df2 = pd.DataFrame(hoy)

df1['hoy'] = df2[1]
df1['adj_covid'] = df1[1] / df1['hoy']

df1.to_csv('covid_mural.csv', index = False)
    






# ---------------------------------------------------------------------------
#       El Norte
# ---------------------------------------------------------------------------

url = 'https://busquedas.gruporeforma.com/elnorte/BusquedasComs.aspx'

# inicia navegacion
driver = webdriver.Chrome() # Chromedrive.exe debe estar en path
driver.get(url)

hoy = [] ; covid = []
i = 0
while i < I:  #hasta Feb 2020
    
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
    i = i + 1

driver.quit()


# Guardar como csv
import pandas as pd
df1 = pd.DataFrame(covid)
df2 = pd.DataFrame(hoy)

df1['hoy'] = df2[1]
df1['adj_covid'] = df1[1] / df1['hoy']

df1.to_csv('covid_elnorte.csv', index = False)
