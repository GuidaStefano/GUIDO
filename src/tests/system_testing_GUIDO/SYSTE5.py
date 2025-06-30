import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

class TestSYSTE5:
    def setup_method(self, method):
        self.driver = webdriver.Firefox()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_sYSTE5(self):
        self.driver.get("http://localhost:3000/")
        self.driver.find_element(By.CSS_SELECTOR, "#\\33 > span").click()
        self.driver.find_element(By.CSS_SELECTOR, ".menu-inspect > .voceMenuText:nth-child(1) span").click()

        element = self.driver.find_element(By.CSS_SELECTOR, ".menu-inspect > .voceMenuText:nth-child(1) span")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

        self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(1)").click()
        self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(1)").send_keys("https://github.com/rubygems/bundler")

        self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(2)").click()
        self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(2)").send_keys("2099-06-29")

        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary:nth-child(1)").click()

        try:
          WebDriverWait(self.driver, 5).until(
              EC.visibility_of_element_located((By.CSS_SELECTOR, "div.div-input .error-date-msg"))
          )
          assert True, "The date must be today or a date in the past"
        except TimeoutException:
          assert False, "System didn't return the correct error"
