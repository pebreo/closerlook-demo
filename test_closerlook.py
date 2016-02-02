import unittest
import requests
from selenium import webdriver

#PHANTOMJS_DRIVER = r'C:\\python27\\phantomjs.exe'

class BaseTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        super(BaseTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(BaseTestCase, cls).tearDownClass()
        cls.driver.quit()

class TestEshots(BaseTestCase):
    
    #@unittest.skip('wip')
    def test_invalid_login(self):
        """ Test invalid login credentials to eshots """
        self.driver.get('https://reporting.eshots.com/pentaho/Login')
        self.driver.find_element_by_id('username').send_keys('invalidname')
        self.driver.find_element_by_id('password').send_keys('invalidname')
        self.driver.find_element_by_id('login-button').click()
        self.driver.save_screenshot('invalid_login.png')
        assert 'Invalid login.' in self.driver.page_source


    def test_empty_form_submission(self):
        """ Test empty form submission """
        self.driver.get('http://closerlook.com/request-demo/')
        self.driver.find_element_by_id('submit').click()
        assert 'Required' in self.driver.page_source


    def test_that_homepage_links_work(self):
        """
        All the homepage links should work.
        For more comprehensive test goto: http://validator.w3.org/checklink
        """
        self.driver.get('http://www.closerlook.com')
        links = self.driver.find_elements_by_xpath('//body//a[string-length(@href)>1]')
        
        # Filter only valid links
        links = [l for l in links if l.get_attribute('href').startswith('http://www.closerlook')]
        
        for link in links:
            href = link.get_attribute('href')
            print "Checking link %s" % href 
            # Use requests to grab headers of the links
            r = requests.get(href)
            assert r.headers
            assert r.status_code == 200

if __name__ == '__main__':
    unittest.main()
