from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import unittest
import time
from time import sleep

# Configurar opciones para el navegador Chrome
options = Options()
# options.add_argument('--headless') # Ejecuta Chrome en modo headless
options.add_argument('--no-sandbox') # Recomendado en entornos de CI como GitHub Actions
options.add_argument('--disable-dev-shm-usage') # Ayuda a evitar algunos errores en contenedores

class AnimeFLVTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(options=options)

    def test_list_animes_en_emision(self):
        browser = self.browser
        browser.maximize_window()
        browser.get("https://www3.animeflv.net/")  

        contenedor = browser.find_element(By.ID, "mCSB_1")
        animes_list = contenedor.find_elements(By.TAG_NAME, "a")  

        res = []
        for anime in animes_list:
            res.append(anime.text)

        self.assertGreater(len(res), 0, "No se encontraron animes en emisión.")

        print("Animes en emisión:")
        for anime in res:
            print(anime)

    def test_busqueda_anime(self):
        browser = self.browser
        browser.maximize_window()
        browser.get("https://www3.animeflv.net/")  
        search = browser.find_element(By.ID, "search-anime")
        search.clear()
        search.send_keys("Naruto")
        search.submit()
        sleep(2)
        results = browser.find_elements(By.CSS_SELECTOR, ".ListAnimes.AX.Rows.A03.C02.D02")  
        self.assertGreater(len(results), 0, "No se encontraron resultados para 'Naruto'.")

    def test_title_text(self):
        browser = self.browser
        browser.get("https://www3.animeflv.net/")  
        title_element = browser.find_element(By.CSS_SELECTOR, "div.Container h1")
        title_text = title_element.text.strip()
        expected_text = "AnimeFLV tu fuente de anime online gratis en HD"
        self.assertEqual(title_text, expected_text, f"El texto del título no coincide. Se encontró: '{title_text}'")
        
    def test_directorio_anime_navigation(self):
        browser = self.browser
        browser.get("https://www3.animeflv.net/")  
        directorio_anime_link = browser.find_element(By.XPATH, "/html/body/div[2]/header/div/div/div/div[2]/nav/ul/li[2]/a")
        directorio_anime_link.send_keys(Keys.ENTER)
        sleep(5)
        title_element = browser.find_element(By.XPATH, "/html/body/div[2]/div/div/div/h1")
        actual_text = title_element.text.strip()
        expected_text = "Lista completa de Animes"
        self.assertEqual(actual_text, expected_text, f"El texto del título no coincide. Se encontró: '{actual_text}'")
    
    def tearDown(self):
        self.browser.quit()


if __name__ == "__main__":
    unittest.main()