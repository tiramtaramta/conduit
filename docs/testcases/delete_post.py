from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


# -------- A015, TC-0024 Saját poszt törlése --------
def test_delete_post():
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

        def delete_post_process():
            my_articles = driver.find_element_by_xpath("//a[starts-with(@href, '#/@')]")
            my_articles.click()

            time.sleep(2)

            articles_list = driver.find_elements_by_tag_name("h1")
            if len(articles_list) > 0:
                articles_list[0].click()
            else:
                print("Ennek a felhasználónak nincsenek bejegyzései")

            time.sleep(3)

            driver.find_element_by_xpath("//*[@id='app']/div/div[1]/div/div/span/button/span").click()

            time.sleep(2)

            # Ellenőrizzük, hogy valóban törlődött-e a bejegyzés
            my_articles.click()

            time.sleep(2)

            new_articles_list = driver.find_elements_by_tag_name("h1")

            assert not new_articles_list[0] == articles_list[
                0], f"Test Failed: Content is not deleted ({articles_list[0]})."

        login_process()

        delete_post_process()

    finally:
        driver.quit()
