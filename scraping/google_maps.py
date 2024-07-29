import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import logging

# Configurer le niveau de log pour ne pas afficher les messages d'erreur non critiques
logging.basicConfig(level=logging.CRITICAL)

# Configuration du navigateur
options = webdriver.FirefoxOptions()
options.headless = True  # Exécuter en mode headless pour plus de rapidité
driver = webdriver.Firefox(options=options)
driver.get('https://www.google.com/maps/@34.0197376,-5.0102272,14z?entry=ttu')

def close_share_window():
    try:
        # Fermer la fenêtre de partage si elle est ouverte
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Fermer" and contains(@class, "OyzoZb")]'))
        )
        close_button.click()
        time.sleep(2)  # Attendre un peu pour s'assurer que la fenêtre se ferme
    except Exception:
        pass  # Ne rien faire si une erreur se produit

def search_place(nom_hopital, delegation):
    try:
        # Fermer la fenêtre de partage au cas où elle serait restée ouverte
        close_share_window()

        # Attendre que la boîte de recherche soit présente
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="searchboxinput"]'))
        )
        
        # Nettoyer le champ de recherche (au cas où)
        search_box.clear()

        # Vérifier si le nom de l'hôpital commence par "hôpital", sinon ajouter "hôpital"
        if not nom_hopital.lower().startswith("hôpital"):
            nom_hopital = "hôpital " + nom_hopital

        # Entrer le texte dans la boîte de recherche
        search_box.send_keys(f"{nom_hopital}, {delegation}" + Keys.RETURN)
        
        # Attendre que les résultats de recherche soient chargés
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="main"]'))
        )
        time.sleep(2)  # Attendre un peu pour s'assurer que les résultats sont bien chargés

        # Cliquer sur le premier résultat de la recherche
        try:
            first_result = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "hfpxzc") and contains(@aria-label, "Lien consulté")]'))
            )
            first_result.click()
        except Exception:
            pass  # Ne rien faire si une erreur se produit

        # Attendre que la page du résultat soit chargée
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="main"]'))
        )
        time.sleep(2)  # Attendre un peu pour s'assurer que la page est bien chargée

        # Utiliser BeautifulSoup pour analyser le HTML
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extraire les informations spécifiques
        rating = extract_info(soup, 'span', {'class': 'ceNzKf', 'role': 'img'}, 'aria-label', "Rating not found")
        hospital_name = extract_text(soup, 'h1', {'class': 'DUwDvf fontHeadlineLarge'}, "Hospital name not found")
        opening_hours = extract_text(soup, 'span', {'style': 'font-weight: 400; color: rgba(24,128,56,1.00);'}, "Opening hours not found")
        website = extract_text_by_index(soup, 'div', {'class': 'Io6YTe fontBodyMedium kR99db'}, 1, "Website not found")
        phone_number = extract_text_by_index(soup, 'div', {'class': 'Io6YTe fontBodyMedium kR99db'}, 2, "Phone number not found")

        # Assurer que les chaînes sont en UTF-8
        rating = ensure_utf8(rating)
        hospital_name = ensure_utf8(hospital_name)
        opening_hours = ensure_utf8(opening_hours)
        website = ensure_utf8(website)
        phone_number = ensure_utf8(phone_number)

        # Afficher les résultats
        print("Rating:", rating)
        print("Hospital Name:", hospital_name)
        print("Opening Hours:", opening_hours)
        print("Website:", website)
        print("Phone Number:", phone_number)

    except Exception as e:
        print(f"Erreur : {e}")

def extract_info(soup, tag, attributes, attribute_name, default_value):
    try:
        element = soup.find(tag, attributes)
        return element[attribute_name] if element else default_value
    except AttributeError:
        return default_value

def extract_text(soup, tag, attributes, default_value):
    try:
        element = soup.find(tag, attributes)
        return element.get_text() if element else default_value
    except AttributeError:
        return default_value

def extract_text_by_index(soup, tag, attributes, index, default_value):
    try:
        elements = soup.find_all(tag, attributes)
        return elements[index].get_text() if len(elements) > index else default_value
    except AttributeError:
        return default_value

def ensure_utf8(text):
    return text.encode('utf-8-sig').decode('utf-8-sig')

# Charger le fichier Excel avec pandas
try:
    df = pd.read_excel('C:\\Users\\hp\\Desktop\\Sante\\Data\\repartition-des-hopitaux.xlsx')

    for index, row in df.iterrows():
        nom_hopital = row['Nom de l\'hôpital']
        delegation = row['Délégation']

        print(f"Recherche pour : {nom_hopital}, {delegation}")
        search_place(nom_hopital, delegation)
        print("\n")

except Exception as e:
    print(f"Erreur lors de la lecture du fichier Excel : {e}")

# Fermer le navigateur à la fin du script
driver.quit()
