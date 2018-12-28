import time
import traceback
import os

from bs4 import BeautifulSoup
from decouple import config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Crawler():
    ''' Navigates a website '''
    base_url = ''

    def __init__(self, base_url):
        base_url = self.base_url
        chrome_bin = os.environ.get('GOOGLE_CHROME_SHIM', None)
        opts = ChromeOptions()
        opts.binary_location = chrome_bin
        self.driver = webdriver.Chrome(executable_path="chromedriver",
                                       chrome_options=opts)

    def navigate_to(self, url):
        self.driver.get(url)

    def shutdown(self):
        self.driver.quit()

    def where_am_i(self):
        return self.driver.page_source


class EcmsCrawler(Crawler):
    base_url = 'http://www.dot14.state.pa.us/ECMS/SVCOMMain'
    cmh_portal_url = 'http://www.dot14.state.pa.us/ECMS/SVMHLSearch?action=SHOWMAINPAGE'
    root_url = 'http://www.dot14.state.pa.us/ECMS/'

    def __init__(self, base_url='http://www.dot14.state.pa.us/ECMS/SVCOMMain'):
        Crawler.__init__(self, base_url)

    def login(self, username, password):
        username_box = self.driver.find_element_by_name("userid")
        password_box = self.driver.find_element_by_name("password")

        username_box.send_keys(username)
        password_box.send_keys(password)

        self.driver.find_element_by_name('login').click()
        WebDriverWait(self.driver, 1).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.accept()

    def go_to_cmh_logs(self, job_number):
        ''' Navigate from Mileage and Hours Portal to Specific Jobs CMH logs'''

        agreement_box = self.driver.find_element_by_name("AGR")

        agreement_box.clear()
        agreement_box.send_keys(job_number)
        # Click the go button once the agreement number is entered.
        self.driver.find_element_by_name("GOCMH").click()

    def download_html(self, agreement_number):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        with open(f"prntf{agreement_number}CMHLOGPage.html", "w") as file:
            file.write(str(soup))

    def current_page_source(self):
        return self.driver.page_source
