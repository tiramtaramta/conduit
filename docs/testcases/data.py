
def login(driver):
  sign_in_btn = driver.find_element_by_xpath('//a[@href="#/login"]')
  sign_in_btn.click()
  email_input = driver.find_element_by_xpath('//input[@placeholder="Email"]')
  password_input = driver.find_element_by_xpath('//input[@placeholder="Password"]')
  email_input.send_keys("user200@hotmail.com")
  password_input.send_keys("Userpass1")
  sign_up_button = driver.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
  sign_up_button.click()

  
