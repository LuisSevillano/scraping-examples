# -*- encoding: utf-8 -*-
#!/usr/bin/Python

import requests
from bs4 import BeautifulSoup
import unicodecsv

# Creamos una función que va a limpiar los Strings
def clean_text(text):
    return (text
            .get_text() # Método de BeautifulSoup que devuelve el texto
            .replace('\n', ' ') # Reemplaza los saltos de línea
            .strip()) # Elimina los espacios al comienzo y al final


# En esta url está la tabla que queremos scrapear
url = "https://es.wikipedia.org/wiki/Anexo:Indicadores_de_las_cityes_de_Am%C3%A9rica_Latina"
resp = requests.get(url)

# Utilizamos BeautifulSoup para parsear la respuesta
soup = BeautifulSoup(resp.content, 'lxml')

# Seleccionamos la tabla de la página en base a dos clases css
table = soup.find('table', attrs = {'class': 'sortable wikitable'})

# Abrimos el csv. Si no existe lo crea
filename = "cityes-por-PIB" + ".csv"
ficherocsv = open(filename, "ab")
writer = unicodecsv.writer(ficherocsv)

rows = table.findAll("tr")
for row in rows:
    # Seleccionamos todos los elementos th y td
    columns = row.findAll(["th", "td"])

    # Accedemos a los valores de las celdas
    # Utilizamos la función clean_text que devuelve el String limpio
    city = clean_text(columns[0])
    country = clean_text(columns[1])
    gdp = clean_text(columns[2])
    gdp_capita = clean_text(columns[3])
    gdp_ppa_capita = clean_text(columns[4])
    population = clean_text(columns[5])

    # Creamos una tupla con los datos
    record = (city, country, gdp, gdp_capita, gdp_ppa_capita, population)

    # Declaramos una lista y añadimos la tupla
    csv_row = []
    csv_row.append(record)

    # Grabamos la fila en el csv
    writer.writerows(csv_row)
