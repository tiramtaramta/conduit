import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def find_element(driver, search_type, value):
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((search_type, value)))
    return element


def basic_login(driver):
    driver.find_element_by_xpath("//a[@href='#/login']").click()

    user_input_data = ["user200", "user200@hotmail.com", "Userpass1"]

    # Bejelentkezési űrlap feltöltése
    for i in range(len(user_input_data) - 1):
        driver.find_element_by_xpath(f"//fieldset[{i + 1}]/input").send_keys(user_input_data[i + 1])

    time.sleep(1)

    driver.find_element_by_tag_name("button").click()

    time.sleep(2)

    # Bejelentkezés tényének ellenőrzése
    username_check = driver.find_element_by_xpath("//a[starts-with(@href, '#/@')]").text
    assert username_check == user_input_data[0], f"Test Failed: User is not logged in ({user_input_data[0]})."

    time.sleep(2)
