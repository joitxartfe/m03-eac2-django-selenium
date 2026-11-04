#from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# Create your tests here.

class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        #service = Service(executable_path="/home/isard/env1/bin/geckodriver")
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
        # creem superusuari
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        # tanquem browser
        # comentar la propera línia si volem veure el resultat de l'execució al navegador
        #cls.selenium.quit()
        super().tearDownClass()

    def test_introduirPreguntesIRespostes(self):
        # anem directament a la pàgina d'accés a l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))
 
        # introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()

        # testejem que hem entrat a l'admin panel comprovant el títol de la pàgina
        self.assertEqual( self.selenium.title , "Site administration | Django site admin" )

        #afegir preguntes
        add_question = self.selenium.find_element(By.XPATH,"//tr[@class='model-question']/td/a[@class='addlink']")
        add_question.click()
        question_input = self.selenium.find_element(By.NAME,"question_text")
        question_input.send_keys('Question1')
        #introduir el dia actual
        self.selenium.find_element(By.LINK_TEXT,"Today").click()
        #introduir l'hora actual
        self.selenium.find_element(By.LINK_TEXT,"Now").click()
        #guardar i introduir un altre
        self.selenium.find_element(By.XPATH,"//input[@value='Save and add another']").click()
        question_input = self.selenium.find_element(By.NAME,"question_text")
        question_input.send_keys('Question2')
        #introduir el dia actual
        self.selenium.find_element(By.LINK_TEXT,"Today").click()
        #introduir l'hora actual
        self.selenium.find_element(By.LINK_TEXT,"Now").click()
        #guardar 
        self.selenium.find_element(By.XPATH,"//input[@value='Save']").click()

        #afegir respostes
        add_choice = self.selenium.find_element(By.XPATH,"//tr[@class='model-choice']/td/a[@class='addlink']")
        add_choice.click()
        question = self.selenium.find_element(By.NAME,"question")
        option = Select(question)
        option.select_by_visible_text("Question1")
        choice_input = self.selenium.find_element(By.NAME,"choice_text")
        choice_input.send_keys('Answer1toQuestion1')
        #guardar i introduir un altre
        self.selenium.find_element(By.XPATH,"//input[@value='Save and add another']").click()
        question = self.selenium.find_element(By.NAME,"question")
        option = Select(question)
        option.select_by_visible_text("Question1")
        choice_input = self.selenium.find_element(By.NAME,"choice_text")
        choice_input.send_keys('Answer2toQuestion1') 
        #guardar i introduir un altre
        self.selenium.find_element(By.XPATH,"//input[@value='Save and add another']").click()
        question = self.selenium.find_element(By.NAME,"question")
        option = Select(question)
        option.select_by_visible_text("Question2")
        choice_input = self.selenium.find_element(By.NAME,"choice_text")
        choice_input.send_keys('Answer1toQuestion2')
        #guardar i introduir un altre
        self.selenium.find_element(By.XPATH,"//input[@value='Save and add another']").click()
        question = self.selenium.find_element(By.NAME,"question")
        option = Select(question)
        option.select_by_visible_text("Question2")
        choice_input = self.selenium.find_element(By.NAME,"choice_text")
        choice_input.send_keys('Answer2toQuestion2')
        #guardar
        self.selenium.find_element(By.XPATH,"//input[@value='Save']").click()

        #comprobar la qunatitat de respostes
        choices_quantity = self.selenium.find_elements(By.CLASS_NAME,"action-select")
        self.assertEqual(len(choices_quantity), 4, "Error, no hi ha 4 respostes")
