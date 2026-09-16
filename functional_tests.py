import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 5


class NewVisitorTest(LiveServerTestCase):

    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Comprar penas de pavão')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Comprar penas de pavão')

        # Maria nota que sua lista tem um URL único
        maria_list_url = self.browser.current_url
        self.assertRegex(maria_list_url, '/lists/.+')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Maria começa uma nova lista
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Comprar penas de pavão')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Comprar penas de pavão')

        maria_list_url = self.browser.current_url

        # Agora um novo usuário, João, entra no site
        # Usamos uma nova sessão de navegador para garantir que nenhum dado de Maria vaze
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # João visita a página inicial. Não há sinal da lista de Maria
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Comprar penas de pavão', page_text)

        # João inicia uma nova lista inserindo um novo item
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Comprar leite')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Comprar leite')

        # João ganha seu próprio URL exclusivo
        joao_list_url = self.browser.current_url
        self.assertRegex(joao_list_url, '/lists/.+')
        self.assertNotEqual(joao_list_url, maria_list_url)

        # Novamente, não há sinal da lista de Maria
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Comprar penas de pavão', page_text)
        self.assertIn('Comprar leite', page_text)