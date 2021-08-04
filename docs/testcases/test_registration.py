from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import random
import time
import csv


# -------- A002, TC-0002 Regisztráció helyes adatokkal --------
def test_registration():
    browser_options = Options()
    browser_options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
    driver.get("http://localhost:1667/#/")

    time.sleep(2)
    random_user_name = "user" + str(random.randint(202, 1000))

    user_input_data = [random_user_name, f"{random_user_name}@hotmail.com", "Userpass1"]

    driver.find_element_by_xpath("//a[@href='#/register']").click()

    # Beviteli mezők feltöltése a random user adatokkal
    for i in range(len(user_input_data)):
        driver.find_element_by_xpath(f"//fieldset[{i + 1}]/input").send_keys(user_input_data[i])
    driver.find_element_by_tag_name("button").click()

    time.sleep(2)

    # Sikeres regisztrációs értesítési ablak szövegének ellenőrzése
    assert driver.find_element_by_class_name("swal-text").text == "Your registration was successful!"

    time.sleep(2)

    # Értesítési ablak bezárása
    driver.find_element_by_xpath("//button[normalize-space()='OK']").click()

    time.sleep(1)

    # Bejelentkezés tényének ellenőrzése
    username_check = driver.find_element_by_xpath("//a[starts-with(@href, '#/@')]").text
    assert username_check == user_input_data[
        0], f"Test Failed: Username did not match expected ({user_input_data[0]})."

    # A létrehozott felhasználó nevének kimentése a későbbi belépésekhez
    with open('registered_users.csv', 'a', encoding="utf-8") as csv_users:
        csv_users.write(random_user_name + ";")

    driver.quit()
