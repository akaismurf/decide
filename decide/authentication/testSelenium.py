from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from base.tests import BaseTestCase

#PARA QUE FUNCIONE ACTIVAR USUARIO ADMIN EN base/tests.py -- metodo setUp
class AdminTestCase(StaticLiveServerTestCase):

    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()            
            
    def tearDown(self):           
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def test_simpleCorrectLogin(self):                    
        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("qwerty",Keys.ENTER)
        
        print(self.driver.current_url)
        #In case of a correct loging, a element with id 'user-tools' is shown in the upper right part
        self.assertTrue(len(self.driver.find_elements_by_id('user-tools'))==1)

    def test_simpleWrongLogin(self):                    
        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element_by_id('id_username').send_keys("WRONG")
        self.driver.find_element_by_id('id_password').send_keys("WRONG")
        self.driver.find_element_by_id('login-form').submit()
        
        print(self.driver.current_url)
        self.assertTrue(len(self.driver.find_elements_by_class_name('errornote'))==1)

    def test_questionCreation(self):                    
        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("qwerty",Keys.ENTER)
        
        print(self.driver.current_url)
        #In case of a correct loging, a element with id 'user-tools' is shown in the upper right part
        self.assertTrue(len(self.driver.find_elements_by_id('user-tools'))==1)
        self.driver.get(f'{self.live_server_url}/admin/voting/question/add/')
        print(self.driver.current_url)

        #se puede mejorar de otras formas pero asi para probar sirve
        self.driver.find_elements_by_tag_name("textarea")[0].send_keys("TestingDesc")
        self.driver.find_elements_by_tag_name("textarea")[1].send_keys("option1")
        self.driver.find_elements_by_tag_name("textarea")[2].send_keys("option2")

        self.driver.find_element_by_xpath('/html/body/div/div[3]/div/form/div/div[2]/input[1]').submit()

        self.assertTrue(len(self.driver.find_elements_by_class_name('success'))==1)

    '''
    #Test created by selenium IDE
    def test_loginCorrect(self):
        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element(By.ID, "id_username").send_keys("tgb")
        self.driver.find_element(By.ID, "id_password").send_keys("decide2021")
        self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
        self.driver.find_element(By.ID, "container").click()
    '''