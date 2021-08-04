from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from basic_function import find_element
import random
import time
import csv


# -------- A004, TC-0010 Bejelentkezés helyes adatokkal --------
def test_login():
    browser_options = Options()
    browser_options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
    driver.get("http://localhost:1667/#/")

    time.sleep(2)


    driver.find_element_by_xpath("//a[@href='#/login']").click()

    user_input_data = ["user200", "user200@hotmail.com", "Userpass1"]

    # Bejelentkezési űrlap feltöltése
    for i in range(len(user_input_data) - 1):
        driver.find_element_by_xpath(f"//fieldset[{i + 1}]/input").send_keys(user_input_data[i + 1])

    time.sleep(1)

    driver.find_element_by_tag_name("button").click()

    time.sleep(2)

    # Bejelentkezés tényének ellenőrzése
    username_check = driver.find_element_by_xpath("//a[@class='nav-link'][starts-with(@href, '#/@')]").text
    assert username_check == user_input_data[0], f"Test Failed: User is not logged in ({user_input_data[0]})."
    driver.quit()
