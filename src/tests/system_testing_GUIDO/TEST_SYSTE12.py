#TEST SYSTE12:  Repository:  https://github.com/netty/netty Data fine:  12/06/2025 -> Error: 'An Error Occurred during the analysis... Please try again later!'#

import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


class TestSYSTE12():
  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_sYSTE12(self):
    self.driver.get("http://localhost:3000/")
    self.driver.set_window_size(1290, 828)
    self.driver.find_element(By.CSS_SELECTOR, "#\\33 > span").click()
    self.driver.find_element(By.CSS_SELECTOR, ".insert-req").click()
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(1)").click()
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(1)").send_keys("https://github.com/netty/netty")
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(2)").click()
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(2)").send_keys("2025-06-12")
    self.driver.find_element(By.CSS_SELECTOR, ".btn-primary:nth-child(1)").click()
    self.driver.find_element(By.CSS_SELECTOR, ".modal-footer > .btn-primary").click()
    self.driver.find_element(By.CSS_SELECTOR, ".menu-inspect > .voceMenuText:nth-child(2) span").click()
    self.driver.find_element(By.CSS_SELECTOR, ".flex-col > div:nth-child(1)").click()

    try:
        error_element = WebDriverWait(self.driver, 720).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".failed-answer .specific-error"))
        )
        if(error_element.text.strip().lower() == ("An Error Occurred during the analysis... Please try again later!").lower()):
          assert True, "The system returned the right error message 'An Error Occurred during the analysis... Please try again later!'"
        else:
          assert False, "The system didn't returned the right error message 'An Error Occurred during the analysis... Please try again later!'"
    except TimeoutException:
        assert False, "The system returned the any error message"

