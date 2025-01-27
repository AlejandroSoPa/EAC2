from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class AdminPanelTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        opts.add_argument("--headless")
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)

        # Creació del superusuari
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        # Tanquem el navegador
        cls.selenium.quit()
        super().tearDownClass()

    def test_admin_login(self):
        # Accedim a la pàgina d'inici de sessió del panell d’administració
        self.selenium.get(f"{self.live_server_url}/admin/login/")

        # Localitzem els camps del formulari de login
        username_input = self.selenium.find_element(By.NAME, "username")
        password_input = self.selenium.find_element(By.NAME, "password")

        # Introduïm les credencials i enviem el formulari
        username_input.send_keys("isard")
        password_input.send_keys("pirineus")
        password_input.send_keys(Keys.RETURN)

        # Comprovem que s’ha iniciat sessió correctament
        self.assertEqual( self.selenium.title , "Site administration | Django site admin" )

    def test_eactest(self):
        # Creació del superusuari
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

        # Accedim a la pàgina d'inici de sessió del panell d’administració
        self.selenium.get(f"{self.live_server_url}/admin/login/")

        # Localitzem els camps del formulari de login
        username_input = self.selenium.find_element(By.NAME, "username")
        password_input = self.selenium.find_element(By.NAME, "password")

        # Introduïm les credencials i enviem el formulari
        username_input.send_keys("isard")
        password_input.send_keys("pirineus")
        password_input.send_keys(Keys.RETURN)

        # Esperem fins que es carregui la pàgina d'administració
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Choices"))
        )

        # Accedim a la pàgina de creació d'enquestes
        self.selenium.find_element(By.XPATH, "//a[@href='/admin/polls/question/add/']").click()

        # Localitzem els camps del formulari
        question_input = self.selenium.find_element(By.NAME, "question_text")
        date_input = self.selenium.find_element(By.NAME, "pub_date_0")
        time_input = self.selenium.find_element(By.NAME, "pub_date_1")

        # Introduïm les dades bàsiques de la pregunta
        question_input.send_keys("Què és millor?")
        date_input.send_keys("2025-01-01")
        time_input.send_keys("12:00:00")

        # Creem 100 opcions (Choices) utilitzant un bucle
        for i in range(100):
            # Localitzem l'input per a la nova opció
            choice_input = self.selenium.find_element(By.NAME, f"choice_set-{i}-choice_text")
            choice_input.send_keys(f"Opció {i + 1}")

            # Afegeix un nou camp per a una altra opció si no és l'última
            if i < 99:
                self.selenium.find_element(By.CSS_SELECTOR, ".add-row a").click()

        # Guardem la pregunta
        self.selenium.find_element(By.NAME, "_save").click()

        # Comprovem que les opcions han estat creades correctament
        question_id = self.selenium.current_url.split("/")[-2]  # Obtenim l'ID de la pregunta creada
        self.selenium.get(f"{self.live_server_url}/admin/polls/question/{question_id}/change/")

        # Esperem que es carreguin les opcions
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_all_elements_located((By.NAME, "choice_set-0-choice_text"))
        )

        choices = self.selenium.find_elements(By.NAME, "choice_set-*-choice_text")
        self.assertEqual(len(choices), 100, "El nombre d'opcions no és correcte")