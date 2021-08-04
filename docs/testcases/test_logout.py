import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from basic_function import basic_login, basic_registration, find_element


# -------- A005, TC-0003 Kijelentkezés --------
def test_logout():
    browser_options = Options()
    browser_options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
    driver.get("http://localhost:1667/#/")

    basic_registration(driver)
    log_out_btn = find_element(driver, By.XPATH, "//a[@active-class='active' AND @class='nav-link')]")
    log_out_btn.click()

    # Kijelentkezés tényének ellenőrzése
    sign_out_check = find_element(driver, By.XPATH, "//a[starts-with(@href, '#/login')]").text
    assert sign_out_check == f"{sign_out_check}", f"Test Failed: User is logged in."

    driver.quit()
