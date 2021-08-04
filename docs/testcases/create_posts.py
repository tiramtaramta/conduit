from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv


# -------- A006, TC-0015 Új adatbevitel helyes adatokkal (sorozatos) --------
def test_create_posts():
    browser_options = Options()
    browser_options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
    driver.maximize_window()

    try:
        driver.get("http://localhost:1667/#/")

        time.sleep(2)

        def login_process():
            driver.find_element_by_xpath("//a[@href='#/login']").click()

            user_input_data = ["user200", "user200@hotmail.com", "Userpass1"]

            time.sleep(1)

            # Bejelentkezési űrlap feltöltése
            for i in range(len(user_input_data) - 1):
                driver.find_element_by_xpath(f"//fieldset[{i + 1}]/input").send_keys(user_input_data[i + 1])

            time.sleep(1)

            driver.find_element_by_tag_name("button").click()

            time.sleep(2)

            # Bejelentkezés tényének ellenőrzése
            username_check = driver.find_element_by_xpath("//a[starts-with(@href, '#/@')]").text
            assert username_check == user_input_data[0], f"Test Failed: User is not logged in ({user_input_data[0]})."

            time.sleep(4)

        def create_posts_process():
            for i in range(1):
                with open('contents.csv') as article_file:
                    csv_reader = csv.reader(article_file, delimiter=';')
                    for row in csv_reader:
                        new_article_data = row

                        # Beviteli űrlap feltöltése
                        driver.find_element_by_xpath("//a[@href='#/editor']").click()
                        time.sleep(4)
                        driver.find_element_by_xpath("//input[@placeholder='Article Title']").send_keys(
                            new_article_data[0])
                        driver.find_element_by_xpath("//input[starts-with(@placeholder,'What')]").send_keys(
                            new_article_data[1])
                        driver.find_element_by_xpath("//textarea[starts-with(@placeholder,'Write')]").send_keys(
                            new_article_data[2])
                        driver.find_element_by_xpath("//input[@placeholder='Enter tags']").send_keys(
                            new_article_data[3])

                        time.sleep(1)

                        driver.find_element_by_css_selector("button[type='submit']").click()

                        time.sleep(2)

                        # Bejegyzés létrejöttének ellenőrzése
                        title_check = driver.find_element_by_tag_name("h1").text
                        assert title_check == new_article_data[
                            0], f"Test Failed: Content title did not match expected ({new_article_data[0]})."

                        time.sleep(4)

        login_process()

        create_posts_process()

    finally:
        driver.quit()
