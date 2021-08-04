from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import csv


# -------- A007, TC-0025 Bejegyzések listájának megtekintése --------
def test_global_feed_list():
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

        def global_feed_list_process():
            driver.find_element_by_xpath("//a[starts-with(@href, '#/')]").click()

            time.sleep(2)

            articles_list = driver.find_elements_by_xpath("//div[@class='article-preview']/a/h1")

            if os.path.exists("titles_list.csv"):
                os.remove("titles_list.csv")
            else:
                pass

            for i in range(len(articles_list)):
                article_title = articles_list[i].text
                with open('titles_list.csv', 'a', encoding="utf-8") as csv_titles:
                    csv_titles.write(f"{article_title};")

            # a lista hosszának ellenőrzése
            with open('titles_list.csv', 'r', encoding="utf-8") as csv_titles2:
                check_articles = csv.reader(csv_titles2, delimiter=';')
                for row in check_articles:
                    check_articles_list = row

            assert len(articles_list) == len(
                check_articles_list) - 1, f"Test Failed: The length of the lists are not exactly the same."

        login_process()

        global_feed_list_process()

    finally:
        driver.quit()
