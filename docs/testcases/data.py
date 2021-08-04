
def login(driver):
  driver.find_element_by_xpath("//a[@href='#/login']").click()
  user_input_data = ["user200", "user200@hotmail.com", "Userpass1"]
  # Bejelentkezési űrlap feltöltése
  for i in range(len(user_input_data) - 1):
      driver.find_element_by_xpath(f"//fieldset[{i + 1}]/input").send_keys(user_input_data[i + 1])

  driver.find_element_by_tag_name("button").click()


  
