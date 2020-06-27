import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class KtoMaLekStartPageTests(unittest.TestCase):
    """
    Scenariusz testowy: Weryfikacja danych dostępowych na stronie https://ktomalek.pl
    """

    @classmethod
    def setUpClass(self):
        self.base_url = 'https://ktomalek.pl/'
        self.driver = webdriver.Chrome(executable_path=r"C:\WSB_PROJECTS\chromedriver.exe")
        self.driver.maximize_window()

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    # weryfikacja czy pod wskazanym adresem url znajduje się zadana nazwa strony lub fragment z zadanej nazwy
    def test_start_page_name(self):
        expected_page_title = 'KtoMaLek'
        driver = self.driver
        driver.get(self.base_url)

        actual_title = driver.title
        print(f'Actual page title on url {driver.current_url} is \'{actual_title}\'')
        self.assertIn(expected_page_title, actual_title,
                         f'Expected title \'{expected_page_title}\' differ from actual \'{actual_title}\' on page url: {self.base_url}')


    # weryfikacja czy menu dostępne w prawym górnym rogu strony głównej zawiera zadaną frazę
    def test_start_page_menu(self):
        menu_button_xpath = "//*[@id='menuToggler']"
        menu_info_elements_xpath = "//*[@id='menuStrap']/div/a"
        expected_menu_element_text = 'Informacje o lekach'
        found_elements_number = 0

        driver = self.driver
        driver.get(self.base_url)

        menu_button = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, menu_button_xpath)),
            f"Menu button element on page: {driver.current_url} not found")
        menu_button.click()
        menu_elements = driver.find_elements_by_xpath(menu_info_elements_xpath)

        for menu_element in menu_elements:
            menu_element_text = menu_element.get_attribute("text")
            if expected_menu_element_text in menu_element_text:
                print(f'Menu element name: {menu_element_text}')
                found_elements_number = found_elements_number + 1

        self.assertEqual(1, found_elements_number,
                         f"Expected text is not found on page {self.base_url}")

