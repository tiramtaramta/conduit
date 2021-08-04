from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv


# -------- A010, TC-0034 Saját profil szerkesztése, képcsere --------
def test_edit_settings():
    browser_options = Options()
    browser_options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
    driver.maximize_window()

    try:
        driver.get("http://localhost:1667/#/")

        user_input_data = ["user200", "user200@hotmail.com", "Userpass1"]

        time.sleep(2)

        def login_process():
            driver.find_element_by_xpath("//a[@href='#/login']").click()

            # user_input_data = ["user200", "user200@hotmail.com", "Userpass1"]

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

        def edit_settings_process():
            driver.find_element_by_xpath("//a[@href='#/settings']").click()

            time.sleep(2)

            # Your Settings oldal megjelenésének ellenőrzése
            settings_check = driver.find_element_by_tag_name("h1").text
            assert settings_check == "Your Settings", f"Test Failed: Page names did not match expected ({settings_check})."

            time.sleep(3)

            # Beolvassuk az előkészített adatokat
            with open('edit_user.csv') as article_file:
                csv_reader = csv.reader(article_file, delimiter=';')
                for row in csv_reader:
                    user_update = row

            time.sleep(2)

            # Feltöltjük az adatokkal a beviteli űrlap egyes sorait
            user_picture = driver.find_element_by_class_name("form-control")
            user_bio = driver.find_element_by_xpath("//textarea[@placeholder='Short bio about you']")

            user_picture.clear()
            user_picture.send_keys(user_update[0])
            user_bio.clear()
            user_bio.send_keys(user_update[1])

            time.sleep(1)

            driver.find_element_by_xpath("//button[normalize-space()='Update Settings']").click()

            time.sleep(2)

            # Sikeres update értesítési ablak szövegének ellenőrzése
            assert driver.find_element_by_class_name("swal-title").text == "Update successful!"

            time.sleep(2)

            # Értesítési ablak bezárása
            driver.find_element_by_xpath("//button[normalize-space()='OK']").click()

            time.sleep(1)

            # Ellenőrizzük a felhasználó profiljában történt változásokat
            driver.find_element_by_xpath("//a[starts-with(@href, '#/@')]").click()

            time.sleep(2)

            img_check = driver.find_element_by_class_name("user-img").get_attribute("src")
            assert img_check == user_update[
                0], f"Test Failed: Image did not match expected ({user_update[0]})."
            user_check = driver.find_element_by_tag_name("h4").text
            assert user_check == user_input_data[
                0], f"Test Failed: User did not match expected ({user_input_data[0]})."
            bio_check = driver.find_element_by_css_selector("div[class='user-info'] p").text
            assert bio_check == user_update[
                1], f"Test Failed: User's bio did not match expected ({user_update[1]})."

            time.sleep(2)

        login_process()

        edit_settings_process()

    finally:
        driver.quit()
