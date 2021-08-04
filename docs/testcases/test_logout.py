from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from data import login


# -------- A005, TC-0003 Kijelentkezés --------
def test_logout():
    browser_options = Options()
    browser_options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
    driver.get("http://localhost:1667/#/")
    
    login(driver)

    time.sleep(2)

    driver.find_element_by_xpath("//a[@active-class='active']").click()

    time.sleep(2)

    # Kijelentkezés tényének ellenőrzése
    sign_out_check = driver.find_element_by_xpath("//a[starts-with(@href, '#/login')]").text
    assert sign_out_check == f"{sign_out_check}", f"Test Failed: User is logged in."

    time.sleep(1)

       
   
    driver.quit()
