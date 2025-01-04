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
        self.selenium.find_element(By.XPATH, "//button[@type='submit' and text()='Log out']")

    def test_create_poll(self):
        # Accedim a la pàgina de creació de la enquesta
        self.selenium.find_element(By.XPATH, "//a[@aria-describedby='polls-question']").click()


        # Localitzem els camps del formulari
        question_input = self.selenium.find_element(By.NAME, "question_text")
        date_input = self.selenium.find_element(By.NAME, "pub_date_0")
        time_input = self.selenium.find_element(By.NAME, "pub_date_1")

        # Introduïm les dades i enviem el formulari
        question_input.send_keys("Què és millor?")
        date_input.send_keys("2021-01-01")
        time_input.send_keys("12:00:00")
        question_input.send_keys(Keys.RETURN)

        # Comprovem que la nova enquesta ha estat creada
        self.selenium.find_element(By.XPATH, "//a[text()='Què és millor?']")

    def test_non_existant_element(self):
        # Intentem trobar un element que no hi hauria de ser
        try:
            self.selenium.find_element(By.XPATH, "//a[text()='Element Inexistent']")
            assert False, "Trobat element que NO hi ha de ser"
        except NoSuchElementException:
            pass
    
    