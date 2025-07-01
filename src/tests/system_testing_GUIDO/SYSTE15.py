#TEST SYSTE15:  Repository:  https://github.com/rubygems/bundler Data fine:  01/01/2019 -> Success: request returned and graph is displayed'##

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


class TestSYSTE15():
  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_sYSTE15(self):
    self.driver.get("http://localhost:3000/")
    self.driver.set_window_size(1290, 828)
    self.driver.find_element(By.CSS_SELECTOR, "#\\33 > span").click()
    self.driver.find_element(By.CSS_SELECTOR, ".insert-req").click()
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(1)").click()
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(1)").send_keys("https://github.com/rubygems/bundler")
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(2)").click()
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(2)").send_keys("2019-01-01")
    self.driver.find_element(By.CSS_SELECTOR, ".btn-primary:nth-child(1)").click()
    self.driver.find_element(By.CSS_SELECTOR, ".modal-footer > .btn-primary").click()
    self.driver.find_element(By.CSS_SELECTOR, ".menu-inspect > .voceMenuText:nth-child(2) span").click()
    self.driver.find_element(By.CSS_SELECTOR, ".flex-col > div:nth-child(1)").click()

    try:
        success_elem = WebDriverWait(self.driver, 720).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".success-answer"))
        )
        success_elem.click()

        time.sleep(5)

        graph_present = self.driver.find_element(By.CSS_SELECTOR, ".graph-div")
        assert graph_present.is_displayed(), "Graph is displayed as expected"
    except TimeoutException:
        assert False, "The system didn't return correct request"

