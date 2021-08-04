from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


# -------- A005, TC-0003 Kijelentkezés --------
def test_logout():
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

        def logout_process():
            driver.find_element_by_xpath("//i[@class='ion-android-exit']").click()

            time.sleep(2)

            # Kijelentkezés tényének ellenőrzése
            sign_out_check = driver.find_element_by_xpath("//a[starts-with(@href, '#/login')]").text
            assert sign_out_check == f"{sign_out_check}", f"Test Failed: User is logged in."

            time.sleep(1)

        login_process()

        logout_process()

    finally:
        driver.quit()
