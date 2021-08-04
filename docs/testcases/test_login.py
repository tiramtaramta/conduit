from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
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

    # Automata regisztrációval létrejött felhasználók beolvasása
    with open('docs/testcases/registered_users.csv') as users_file:
        csv_reader = csv.reader(users_file, delimiter=';')
        for row in csv_reader:
            users_list = row

    # Random felhasználó kiválasztása a bejelentkezéshez
    random_user_index = random.randint(0, len(users_list) - 1)
    random_user_name = users_list[random_user_index]
    user_input_data = [random_user_name, f"{random_user_name}@hotmail.com", "Userpass1"]

    # Bejelentkezési űrlap feltöltése
    for i in range(len(user_input_data) - 1):
        driver.find_element_by_xpath(f"//fieldset[{i + 1}]/input").send_keys(user_input_data[i + 1])

    time.sleep(1)

    driver.find_element_by_tag_name("button").click()

    time.sleep(2)

    # Bejelentkezés tényének ellenőrzése
    username_check = find_element(driver, By.XPATH, "//a[@class='nav-link'][starts-with(@href, '#/@')]").text
    assert username_check == user_input_data[0], f"Test Failed: User is not logged in ({user_input_data[0]})."
    driver.quit()
