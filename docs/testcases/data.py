from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def find_element(driver, search_type, value):
    element = WebDriverWait(
        driver, 10).until(
        EC.visibility_of_element_located((search_type, value))
    )
    return element

def registration201(driver):
    user_input_data = ["user201", "user201@hotmail.com", "Userpass1"]

    driver.find_element_by_xpath("//a[@href='#/register']").click()

    # Beviteli mezők feltöltése a random user adatokkal
    for i in range(len(user_input_data)):
        driver.find_element_by_xpath(f"//fieldset[{i + 1}]/input").send_keys(user_input_data[i])
    driver.find_element_by_tag_name("button").click()
    time.sleep(2)
    # Értesítési ablak bezárása
    driver.find_element_by_xpath("//button[normalize-space()='OK']").click()


def login(driver):
    sign_in_btn = driver.find_element_by_xpath('//a[@href="#/login"]')
    sign_in_btn.click()
    email_input = driver.find_element_by_xpath('//input[@placeholder="Email"]')
    password_input = driver.find_element_by_xpath('//input[@placeholder="Password"]')
    email_input.send_keys("user200@hotmail.com")
    password_input.send_keys("Userpass1")
    sign_up_button = driver.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
    sign_up_button.click()


  
