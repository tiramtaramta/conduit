from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.common.exceptions import NoSuchElementException


# -------- A028, TC-0037 Cookie kezelési tájékoztató --------
def test_cookie_accept():
    browser_options = Options()
    browser_options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
    driver.get("http://localhost:1667/#/")

    time.sleep(2)

    assert driver.find_element_by_id("cookie-policy-panel").is_displayed()

    # Cookie-k elfogadása folyamat
    driver.find_element_by_xpath(
        "//button[@class='cookie__bar__buttons__button cookie__bar__buttons__button--accept']").click()

    time.sleep(2)

    # # Cookie-k elutasítása folyamat
    # driver.find_element_by_xpath(
    #     "//button[@class='cookie__bar__buttons__button cookie__bar__buttons__button--decline']").click()
    #
    # time.sleep(2)

    def check_cookie_policy_by_id(id):
        try:
            driver.find_element_by_id(id)

            time.sleep(2)

        except NoSuchElementException:
            return True
        return False

    check_cookie_policy_by_id("cookie-policy-panel")

    driver.quit()
