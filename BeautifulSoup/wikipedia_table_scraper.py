# -*- encoding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import unicodecsv

# Function that cleans each cells and return as plain string
def clean_text(text):
    return (text
            .get_text()
            .replace('\n', ' ')
            .strip())



url = "https://es.wikipedia.org/wiki/Anexo:Indicadores_de_las_cityes_de_Am%C3%A9rica_Latina"
resp = requests.get(url)

soup = BeautifulSoup(resp.content, 'lxml')

table = soup.find('table', attrs = {'class': 'sortable wikitable'})

filename = "cities-per-PIB" + ".csv"
ficherocsv = open(filename, "ab")
writer = unicodecsv.writer(ficherocsv)

rows = table.findAll("tr")
for row in rows:
    columns = row.findAll(["th", "td"])

    city = clean_text(columns[0])
    country = clean_text(columns[1])
    gdp = clean_text(columns[2])
    gdp_capita = clean_text(columns[3])
    gdp_ppa_capita = clean_text(columns[4])
    population = clean_text(columns[5])

    record = (city, country, gdp, gdp_capita, gdp_ppa_capita, population)

    csv_row = []
    csv_row.append(record)

    writer.writerows(csv_row)
