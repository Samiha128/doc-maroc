import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def scrape_doctor_profile(driver, profile_url, csv_writer):
    try:
       
        driver.get(profile_url)

       
        time.sleep(2) 
        try:
            show_phone_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "show_phone_number"))
            )
            show_phone_button.click()

          
            phone_number_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "showPhoneNumberAboveFooter"))
            )

            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            phone_number = soup.find('span', id='showPhoneNumberAboveFooter').text.strip()

          
            specialty = soup.find('h2', class_='ab_doc_jurisdiction font-tm').text.strip()
            doctor_name = soup.find('span', class_='doctor_name').text.strip()

           
            print(f"Spécialité : {specialty}")
            print(f"Nom du médecin : {doctor_name}")
            print(f"Numéro de téléphone : {phone_number}")

            csv_writer.writerow([specialty, doctor_name, phone_number])

        except Exception as e:
            print(f"Numéro de téléphone non disponible pour {profile_url}")

    except Exception as e:
        print(f"Une erreur s'est produite lors du scraping de {profile_url} : {e}")

options = Options()
options.headless = True  
driver = webdriver.Firefox(options=options)


page_26_url = 'https://www.doctori.ma/fr/medecin?page=84'
driver.get(page_26_url)


with open('medecins4.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    csv_writer = csv.writer(csvfile)

    try:
       
        csv_writer.writerow(['Spécialité', 'Nom du médecin', 'Numéro de téléphone'])

        
        profile_links = []
        elements = WebDriverWait(driver, 20).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='profil_left']/a[@class='profil_img']"))
        )
        for element in elements:
            profile_links.append(element.get_attribute('href'))

       
        for profile_url in profile_links:
            scrape_doctor_profile(driver, profile_url, csv_writer)
            print("--------------------------------------------------")

      
        time.sleep(2)

       
        for page_num in range(85, 418):
            try:
               
                next_page_url = f"https://www.doctori.ma/fr/medecin?page={page_num}"
                driver.get(next_page_url)

               
                time.sleep(2)

               
                elements = WebDriverWait(driver, 20).until(
                    EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='profil_left']/a[@class='profil_img']"))
                )
                profile_links = [element.get_attribute('href') for element in elements]

                for profile_url in profile_links:
                    scrape_doctor_profile(driver, profile_url, csv_writer)
                    print("--------------------------------------------------")

            except Exception as e:
                print(f"Fin du scraping : {e}")
                break

    finally:
      
        driver.quit()
