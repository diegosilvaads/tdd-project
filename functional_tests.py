from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Maria acessa a página inicial do app To-Do
        self.browser.get('http://localhost:8000')

        # Ela nota que o título e o cabeçalho mencionam To-Do
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # Ela é convidada a inserir um item de tarefa imediatamente
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Ela digita "Comprar penas de pavão"
        inputbox.send_keys('Comprar penas de pavão')

        # Quando ela tecla Enter, a página é atualizada
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # A página agora lista "1: Comprar penas de pavão" como um item
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertTrue(
            any(row.text == '1: Comprar penas de pavão' for row in rows),
            f"O novo item não apareceu na tabela. O conteúdo era:\n{table.text}"
        )

        # Satisfeita, ela vai dormir