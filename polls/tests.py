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
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

        self.selenium.get(f"{self.live_server_url}/admin/login/")
        username_input = self.selenium.find_element(By.NAME, "username")
        password_input = self.selenium.find_element(By.NAME, "password")

        username_input.send_keys("isard")
        password_input.send_keys("pirineus")
        password_input.send_keys(Keys.RETURN)

        # Casos para las dos preguntas
        preguntas = [
            {"texto": "Pregunta 1: 100 opciones", "opciones": 100},
            {"texto": "Pregunta 2: 1 opción", "opciones": 1},
        ]

        for pregunta in preguntas:
            # Acceder a la página de creación de encuestas
            self.selenium.find_element(By.XPATH, "//a[@href='/admin/polls/question/add/']").click()

            # Localizar los campos del formulario
            question_input = self.selenium.find_element(By.NAME, "question_text")
            date_input = self.selenium.find_element(By.NAME, "pub_date_0")
            time_input = self.selenium.find_element(By.NAME, "pub_date_1")

            # Rellenar los datos de la pregunta
            question_input.send_keys(pregunta["texto"])
            date_input.send_keys("2025-01-01")
            time_input.send_keys("12:00:00")

            for i in range(pregunta["opciones"]):
                # Localizar el campo para la opción
                choice_input = self.selenium.find_element(By.NAME, f"choice_set-{i}-choice_text")
                choice_input.send_keys(f"Opción {i + 1}")

                # Añadir una nueva fila si no es la última opción
                if i < pregunta["opciones"] - 1:
                    self.selenium.find_element(By.CSS_SELECTOR, ".add-row a").click()

            # Guardar la pregunta
            self.selenium.find_element(By.NAME, "_save").click()

        # Acceder al modelo de opciones (Choices)
        self.selenium.find_element(By.XPATH, "//th[@id='polls-choice']/a").click()

        # Contar todas las opciones disponibles en el modelo
        choices = self.selenium.find_elements(By.XPATH, "//th[@class='field-__str__']/a")
        total_opciones_esperadas = sum(p["opciones"] for p in preguntas)

        # Verificar que el total de opciones es correcto
        self.assertEqual(
            len(choices), total_opciones_esperadas, f"El número total de opciones no es correcto. Esperado: {total_opciones_esperadas}, Encontrado: {len(choices)}"
        )

            
            

