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
        # Comentar la següent línia si es vol veure el resultat al navegador
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
        self.selenium.find_element(By.XPATH, "//a[text()='Log out']")

    def test_element_no_exists(self):
        # Intentem trobar un element que no hi hauria de ser
        try:
            self.selenium.find_element(By.XPATH, "//a[text()='Element Inexistent']")
            assert False, "Trobat element que NO hi ha de ser"
        except NoSuchElementException:
            pass
