import unittest
import requests
from selenium import webdriver
from pyvirtualdisplay import Display


#PHANTOMJS_DRIVER = r'C:\\python27\\phantomjs.exe'

class BaseTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.display = Display(visible=0, size=(1024, 768)).start()
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        super(BaseTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(BaseTestCase, cls).tearDownClass()
        cls.driver.quit()
        cls.display.stop()

class TestCloserlook(BaseTestCase):
    
    #@unittest.skip('wip')
    def test_searchterm_not_found(self):
        """ Expect no search results when given a nonsense search term """
        self.driver.get('http://closerlook.com')
        self.driver.find_element_by_id('menu-search').click()
        self.driver.find_element_by_id('username').send_keys('thissearchtermwillnotbefound')
        self.driver.save_screenshot('noresultsfound_result.png')
        assert 'No results were found.' in self.driver.page_source


    def test_blank_searchterm(self):
        """ Expect redirect to mainpaige when given a blank search term """
        self.driver.get('http://closerlook.com')
        self.driver.find_element_by_id('menu-search').click()
        self.driver.find_element_by_id('username').send_keys('')
        self.driver.save_screenshot('redirect_result.png')
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
