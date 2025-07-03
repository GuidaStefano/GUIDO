#TEST SYSTE1:  Repository: https://github.com/user Data fine: 29/06/2025 -> Error: Errore Please enter a valid GitHub repository URL (https://github.com/username/repo)#

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

class TestSYSTE1:
    def setup_method(self, method):
        self.driver = webdriver.Firefox()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_sYSTE1(self):
        self.driver.get("http://localhost:3000/")
        self.driver.find_element(By.CSS_SELECTOR, "#\\33 > span").click()
        self.driver.find_element(By.CSS_SELECTOR, ".insert-req").click()

        element = self.driver.find_element(By.CSS_SELECTOR, ".menu-inspect > .voceMenuText:nth-child(1) span")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

        self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(1)").click()
        self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(1)").send_keys("https://github.com/user")

        self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(2)").click()
        self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(2)").send_keys("2025-06-29")

        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary:nth-child(1)").click()

        try:
            error_element = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".error-msg"))
            )
            if(error_element.text.strip().lower() == ("Please enter a valid GitHub repository URL (https://github.com/username/repo)").strip().lower()):
              assert True, "Returned error Please enter a valid GitHub repository URL (https://github.com/user)"
            else:
              assert False, "System didn't return the correct error"
        except TimeoutException:
            assert False, "System didn't return the correct error"
