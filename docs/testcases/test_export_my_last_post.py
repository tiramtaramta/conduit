from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


# -------- A029 Adatok lementése felületről --------
def test_export_my_last_post():
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

        def export_my_last_post_process():
            driver.find_element_by_xpath("//a[starts-with(@href, '#/@')]").click()

            time.sleep(2)

            articles_list = driver.find_elements_by_tag_name("h1")

            if os.path.exists("my_last_article.txt"):
                os.remove("my_last_article.txt")
            else:
                pass

            articles_list[0].click()

            time.sleep(2)

            article_title = driver.find_element_by_tag_name("h1").text
            article_text = driver.find_element_by_tag_name("p").text
            with open("my_last_article.txt", "a") as my_txt:
                my_txt.write(f"{article_title};{article_text};\n")

            time.sleep(3)

            # a kiírt tartalom ellenőrzése
            with open("my_last_article.txt", "r") as my_txt2:
                my_txt = my_txt2.readline()
                my_txt_list = my_txt.split(";")

            assert my_txt_list[0] == article_title, f"Test Failed: Content title is not exported."
            assert my_txt_list[1] == article_text, f"Test Failed: Content text is not exported."

        login_process()

        export_my_last_post_process()

    finally:
        driver.quit()
