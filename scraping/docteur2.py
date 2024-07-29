from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time
import openpyxl


options = Options()
options.headless = True 
driver = webdriver.Firefox(options=options)

base_url = 'https://www.doctori.ma/fr/medecin?page=83'
driver.get(base_url)

time.sleep(5)

data = {
    'Nom': [],
    'Adresse': []
}

def extract_data(soup):
    noms = soup.find_all('span', class_='dr-name-value')
    adresses = soup.find_all('span', class_='adresse_doc')

    for nom, adresse in zip(noms, adresses):
        data['Nom'].append(nom.get_text(strip=True))
        data['Adresse'].append(adresse.get_text(strip=True))

page_num = 83
while page_num <= 417:
   
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    print(f"Page {page_num} :")
    extract_data(soup)

    next_page_link = None
    try:
        next_page_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//a[@class='page-link' and text()='{page_num + 1}']")))
    except:
        break 
    if next_page_link:
        next_page_url = next_page_link.get_attribute('href')
        driver.get(next_page_url)
        time.sleep(5)  
        page_num += 1
    else:
        break 
driver.quit()

df = pd.DataFrame(data)

csv_file = 'doctori_data1.csv'
df.to_csv(csv_file, index=False, encoding='utf-8-sig', quoting=csv.QUOTE_ALL)

excel_file = 'doctori_data1.xlsx'
wb = openpyxl.Workbook()
ws = wb.active
with open(csv_file, 'r', encoding='utf-8-sig') as f:
    for row in csv.reader(f):
        ws.append(row)
wb.save(excel_file)

print(f"Données extraites et enregistrées dans {excel_file} avec le format utf-8-sig")
