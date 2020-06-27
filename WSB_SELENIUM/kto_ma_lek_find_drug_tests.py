import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Dane testowe
city_name = 'Katowice'
street_name = 'Wyszyńskiego 7'
bad_drug_name = 'nieznany lek'
drug_name = "ketonal"   #'aspir' #'nieznany lek'
error_drug_info = 'Brak wyników wyszukiwania.'

class KtoMaLekFindDrugTests(unittest.TestCase):
    """
    Scenariusz testowy: Wyszukanie na stronie https://ktomalek.pl we wskazanej lokalizacji leku według zadanego wzorca 
    """

    @classmethod
    def setUpClass(self):
        self.driver = webdriver.Chrome(executable_path=r"C:\WSB_PROJECTS\chromedriver.exe")
        self.driver.maximize_window()
        self.driver.get('https://ktomalek.pl/')
        self.driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
        sleep(3)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def test_find_drug_in_localization(self):
        # Lokalizatory
        change_address_xpath = '//*[@id="krok_1_linked"]/a'
        address_input_box_xpath = '//*[@id="searchAdresu"]'
        search_drug_input_xpath = '//*[@id="search"]'
        drugs_name_list_xpath = '//*[@class="toggle-box hover-box"]//h2'
        # drugs_name_list_xpath_2 = '//*[@class="nazwaLeku"]'
        no_drugs_xpath = '//*[@id="brakLekowMessage"]'

        drugs_name_rozwin_xpath = '//*[@class="switch-on"]/*[@class="tab:u"]'

        driver = self.driver

        # Kliknij w "1" - "Podaj lokalizacje" / "Wybrana lokalizacja"
        # Zaczekaj max. 30 s. aż pole będzie aktywne
        change_localization = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, change_address_xpath)),
            f'Change adress localization site on page: {driver.current_url} not found')
        change_localization.click()

        # Kliknij w pole "Wpisz miasto i ulicę"; zaczekaj aż pole będzie aktywne"
        enter_address = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, address_input_box_xpath)),
            f'Input address box on page: {driver.current_url} not found')
        # Wprowadź adres
        adress_name = city_name + ', ' + street_name
        enter_address.send_keys(adress_name)
        enter_address.send_keys(Keys.ENTER)

        # Zaczekaj aż uaktywni się pole do wprowadzania leku i wprowadź nazwę poszukiwanego leku
        enter_drug = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, search_drug_input_xpath)),
            f'Input drug box on page: {driver.current_url} not found')
        enter_drug.send_keys(drug_name)
        enter_drug.send_keys(Keys.ENTER)


        # drugs_list = WebDriverWait(driver, 20).until(
        #     EC.presence_of_all_elements_located((By.XPATH, drugs_name_list_xpath)),
        #     f'Drug \'{drug_name}\' on page: {driver.current_url} not found')
        #
        # rozwin_all = driver.find_elements_by_xpath(drugs_name_rozwin_xpath)
        # print(f'{len(rozwin_all)}')
        # for i in range(len(rozwin_all)):
        #     print(f'{rozwin_all[i]}')
        #     # rozwin_all[i].send_keys(Keys.ENTER)


        # Zaczekaj aż strona zwróci listę wyszukanych pozycji
        # Jeżeli lek nie zostanie odnaleziony zwróć komunikat o braku leku
        try:
            drugs_list = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, drugs_name_list_xpath)),
                f'Drug \'{drug_name}\' on page: {driver.current_url} not found')

        except:
            error_notice = driver.find_element_by_xpath(no_drugs_xpath)
            print(error_notice.text)
            self.assertEqual(error_notice.text, error_drug_info)

        else:
            sleep(2)
            # Przejdz przez każdy znaleziony element z listy i zweryfikuj czy nazwa poszukiwanego leku zawiera się w nazwie z każdej ze znalezionej pozycji;
            # wypisz numer i nazwę znalezionej pozycji
            for i in range(len(drugs_list)):
                drug_name_text = drugs_list[i].get_attribute("textContent")
                print(f"{i + 1} drug's name: {drug_name_text}")
                with self.subTest(drug_name_text):
                    self.assertIn(drug_name.upper(), drug_name_text,
                                  f'Drug name {drug_name} not contain in {drug_name_text}')

        # Scroll bottom to up
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(3)
        driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
        sleep(3)
