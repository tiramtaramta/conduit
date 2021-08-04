from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import math


# -------- A007, TC-0025 Bejegyzések listájának megtekintése (lapozóval) --------
def test_global_feed_pagination():
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

        def global_feed_pagination_process():
            driver.find_element_by_xpath("//a[starts-with(@href, '#/')]").click()

            time.sleep(2)

            articles_list = driver.find_elements_by_xpath("//div[@class='article-preview']/a/h1")

            # lapozógombok használata
            pages = driver.find_elements_by_class_name("page-link")

            for page in pages:
                page.click()
                time.sleep(1)

            # Az oldal bejárásának ellenőrzése
            assert len(pages) == int(math.ceil(
                len(articles_list) / 10)), f"Test Failed: The length of the list and pagination not exactly the same."

        login_process()

        global_feed_pagination_process()

    finally:
        driver.quit()
