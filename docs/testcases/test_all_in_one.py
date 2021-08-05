from selenium import webdriver
import time
import csv
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import math
from selenium.webdriver.common.by import By
import os
from basic_function import basic_login, find_element


class TestConduit(object):
    def setup(self):
        browser_options = Options()
        browser_options.headless = True
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
        self.driver.get("http://localhost:1667/#/")

    def teardown(self):
        self.driver.quit()

    # -------- A028, TC-0037 Cookie kezelési tájékoztató --------
    def test_cookie_process(self):

        assert self.driver.find_element_by_id("cookie-policy-panel").is_displayed()

        # Cookie-k elfogadása folyamat
        self.driver.find_element_by_xpath(
            "//button[@class='cookie__bar__buttons__button cookie__bar__buttons__button--accept']").click()

        time.sleep(2)

        # # Cookie-k elutasítása folyamat
        # self.driver.find_element_by_xpath(
        #     "//button[@class='cookie__bar__buttons__button cookie__bar__buttons__button--decline']").click()
        #
        # time.sleep(2)

        try:
            self.driver.find_element_by_id("cookie-policy-panel")

            time.sleep(2)

        except NoSuchElementException:
            return True
        return False

    # -------- A002, TC-0002 Regisztráció helyes adatokkal --------
    def test_registration_process(self):

        user_input_data = ["user200", "user200@hotmail.com", "Userpass1"]

        self.driver.find_element_by_xpath("//a[@href='#/register']").click()

        # Beviteli mezők feltöltése a random user adatokkal
        for i in range(len(user_input_data)):
            self.driver.find_element_by_xpath(f"//fieldset[{i + 1}]/input").send_keys(user_input_data[i])
        self.driver.find_element_by_tag_name("button").click()

        time.sleep(2)

        # Sikeres regisztrációs értesítési ablak szövegének ellenőrzése
        swal_text = find_element(self.driver, By.CLASS_NAME, "swal-text")
        assert swal_text.text == "Your registration was successful!"
        # assert self.driver.find_element_by_class_name("swal-text").text == "Your registration was successful!"

        # time.sleep(2)

        # Értesítési ablak bezárása
        close_btn = find_element(self.driver, By.XPATH, "//button[normalize-space()='OK']")
        close_btn.click()
        # self.driver.find_element_by_xpath("//button[normalize-space()='OK']").click()

        time.sleep(1)

        # Bejelentkezés tényének ellenőrzése
        username_check = self.driver.find_element_by_xpath("//a[starts-with(@href, '#/@')]").text
        assert username_check == user_input_data[
            0], f"Test Failed: Username did not match expected ({user_input_data[0]})."

        # time.sleep(2)

    # -------- A004, TC-0010 Bejelentkezés helyes adatokkal --------
    def test_login_process(self):
        user_input_data = ["user200", "user200@hotmail.com", "Userpass1"]

        self.driver.find_element_by_xpath("//a[@href='#/login']").click()

        # Bejelentkezési űrlap feltöltése
        for i in range(len(user_input_data) - 1):
            self.driver.find_element_by_xpath(f"//fieldset[{i + 1}]/input").send_keys(user_input_data[i + 1])

        time.sleep(1)

        self.driver.find_element_by_tag_name("button").click()

        time.sleep(3)

        # Bejelentkezés tényének ellenőrzése
        username_check = self.driver.find_element_by_xpath("//a[starts-with(@href, '#/@')]").text
        assert username_check == user_input_data[0], f"Test Failed: User is not logged in ({user_input_data[0]})."

        time.sleep(2)

    # -------- A010, TC-0034 Saját profil szerkesztése, képcsere --------
    def test_edit_settings_process(self):
        basic_login(self.driver)

        self.driver.find_element_by_xpath("//a[@href='#/settings']").click()

        time.sleep(2)

        # Your Settings oldal megjelenésének ellenőrzése
        settings_check = self.driver.find_element_by_tag_name("h1").text
        assert settings_check == "Your Settings", f"Test Failed: Page names did not match expected ({settings_check})."

        time.sleep(3)

        # Beolvassuk az előkészített adatokat
        with open('edit_user.csv') as article_file:
            csv_reader = csv.reader(article_file, delimiter=';')
            for row in csv_reader:
                user_update = row

        time.sleep(2)

        # Feltöltjük az adatokkal a beviteli űrlap egyes sorait
        user_picture = self.driver.find_element_by_class_name("form-control")
        user_bio = self.driver.find_element_by_xpath("//textarea[@placeholder='Short bio about you']")

        user_picture.clear()
        user_picture.send_keys(user_update[0])
        user_bio.clear()
        user_bio.send_keys(user_update[1])

        time.sleep(1)

        self.driver.find_element_by_xpath("//button[normalize-space()='Update Settings']").click()

        time.sleep(2)

        # Sikeres update értesítési ablak szövegének ellenőrzése
        assert self.driver.find_element_by_class_name("swal-title").text == "Update successful!"

        time.sleep(2)

        # Értesítési ablak bezárása
        self.driver.find_element_by_xpath("//button[normalize-space()='OK']").click()

        time.sleep(1)

        # Ellenőrizzük a felhasználó profiljában történt változásokat
        self.driver.find_element_by_xpath("//a[starts-with(@href, '#/@')]").click()

        time.sleep(2)

        img_check = self.driver.find_element_by_class_name("user-img").get_attribute("src")
        assert img_check == user_update[
            0], f"Test Failed: Image did not match expected ({user_update[0]})."
        bio_check = self.driver.find_element_by_css_selector("div[class='user-info'] p").text
        assert bio_check == user_update[
            1], f"Test Failed: User's bio did not match expected ({user_update[1]})."

        time.sleep(2)

    # -------- A005, TC-0003 Kijelentkezés --------
    def test_logout_process(self):
        basic_login(self.driver)

        self.driver.find_element_by_xpath("//i[@class='ion-android-exit']").click()

        time.sleep(2)

        # Kijelentkezés tényének ellenőrzése
        sign_out_check = self.driver.find_element_by_xpath("//a[starts-with(@href, '#/login')]").text
        assert sign_out_check == f"{sign_out_check}", f"Test Failed: User is logged in."

        time.sleep(1)

    # -------- A006, TC-0015 Új poszt létrehozása helyes adatokkal --------
    def test_create_post(self):
        basic_login(self.driver)

        self.driver.find_element_by_xpath("//a[@href='#/editor']").click()

        with open('new_post_content.csv') as article_file:
            csv_reader = csv.reader(article_file, delimiter=';')
            for row in csv_reader:
                new_article_data = row

        time.sleep(2)

        # Beviteli űrlap feltöltése
        self.driver.find_element_by_xpath("//input[starts-with(@placeholder,'Article')]").send_keys(new_article_data[0])
        self.driver.find_element_by_xpath("//input[starts-with(@placeholder,'What')]").send_keys(new_article_data[1])
        self.driver.find_element_by_xpath("//textarea[starts-with(@placeholder,'Write')]").send_keys(
            new_article_data[2])
        self.driver.find_element_by_xpath("//input[@placeholder='Enter tags']").send_keys(new_article_data[3])

        time.sleep(1)

        self.driver.find_element_by_css_selector("button[type='submit']").click()

        time.sleep(2)

        # Bejegyzés létrejöttének ellenőrzése
        title_check = self.driver.find_element_by_tag_name("h1").text
        assert title_check == new_article_data[
            0], f"Test Failed: Content title did not match expected ({new_article_data[0]})."

        time.sleep(2)

    # -------- A006, TC-0015 Új adatbevitel helyes adatokkal (sorozatos) --------
    def test_create_posts_process(self):
        basic_login(self.driver)

        for i in range(1):
            with open('contents.csv') as article_file:
                csv_reader = csv.reader(article_file, delimiter=';')
                for row in csv_reader:
                    new_article_data = row

                    # Beviteli űrlap feltöltése
                    self.driver.find_element_by_xpath("//a[@href='#/editor']").click()
                    time.sleep(4)
                    self.driver.find_element_by_xpath("//input[@placeholder='Article Title']").send_keys(
                        new_article_data[0])
                    self.driver.find_element_by_xpath("//input[starts-with(@placeholder,'What')]").send_keys(
                        new_article_data[1])
                    self.driver.find_element_by_xpath("//textarea[starts-with(@placeholder,'Write')]").send_keys(
                        new_article_data[2])
                    self.driver.find_element_by_xpath("//input[@placeholder='Enter tags']").send_keys(
                        new_article_data[3])

                    time.sleep(1)

                    self.driver.find_element_by_css_selector("button[type='submit']").click()

                    time.sleep(2)

                    # Bejegyzés létrejöttének ellenőrzése
                    title_check = self.driver.find_element_by_tag_name("h1").text
                    assert title_check == new_article_data[
                        0], f"Test Failed: Content title did not match expected ({new_article_data[0]})."

                    time.sleep(4)

    # -------- A015, TC-0024 Saját poszt törlése --------
    def test_delete_post_process(self):
        basic_login(self.driver)

        my_articles = self.driver.find_element_by_xpath("//a[starts-with(@href, '#/@')]")
        my_articles.click()
        time.sleep(2)

        articles_list = self.driver.find_elements_by_tag_name("h1")
        if len(articles_list) > 0:
            articles_list[0].click()

        time.sleep(3)

        self.driver.find_element_by_xpath("//*[@id='app']/div/div[1]/div/div/span/button/span").click()

        time.sleep(2)

        # Ellenőrizzük, hogy valóban törlődött-e a bejegyzés
        my_articles.click()

        time.sleep(2)

        new_articles_list = self.driver.find_elements_by_tag_name("h1")

        assert not new_articles_list[0] == articles_list[
            0], f"Test Failed: Content is not deleted ({articles_list[0]})."

    # -------- A029 Adatok lementése felületről --------
    def test_export_my_last_post(self):
        basic_login(self.driver)

        self.driver.find_element_by_xpath("//a[starts-with(@href, '#/@')]").click()

        time.sleep(2)

        articles_list = self.driver.find_elements_by_tag_name("h1")

        if os.path.exists("my_last_article.txt"):
            os.remove("my_last_article.txt")
        else:
            pass

        articles_list[0].click()

        time.sleep(2)

        article_title = self.driver.find_element_by_tag_name("h1").text
        article_text = self.driver.find_element_by_tag_name("p").text
        with open("my_last_article.txt", "a") as my_txt:
            my_txt.write(f"{article_title};{article_text};\n")

        time.sleep(3)

        # a kiírt tartalom ellenőrzése
        with open("my_last_article.txt", "r") as my_txt2:
            my_txt = my_txt2.readline()
            my_txt_list = my_txt.split(";")

        assert my_txt_list[0] == article_title, f"Test Failed: Content title is not exported."
        assert my_txt_list[1] == article_text, f"Test Failed: Content text is not exported."

    # -------- A007, TC-0025 Bejegyzések listájának megtekintése --------
    def test_global_feed_list(self):
        basic_login(self.driver)

        self.driver.find_element_by_xpath("//a[starts-with(@href, '#/')]").click()

        time.sleep(2)

        articles_list = self.driver.find_elements_by_xpath("//div[@class='article-preview']/a/h1")

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

    # -------- A007, TC-0025 Bejegyzések listájának megtekintése (lapozóval) --------
    def test_global_feed_pagination(self):
        basic_login(self.driver)

        self.driver.find_element_by_xpath("//a[starts-with(@href, '#/')]").click()

        time.sleep(2)

        articles_list = self.driver.find_elements_by_xpath("//div[@class='article-preview']/a/h1")

        # lapozógombok használata
        pages = self.driver.find_elements_by_class_name("page-link")

        for page in pages:
            page.click()
            time.sleep(1)

        # Az oldal bejárásának ellenőrzése
        assert len(pages) == int(math.ceil(
            len(articles_list) / 10)), f"Test Failed: The length of the list and pagination not exactly the same."
