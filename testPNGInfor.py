from selenium import webdriver
from selenium.webdriver.common.by import By

def test_eight_components():
    driver = webdriver.Chrome()

    driver.get("http://127.0.0.1:7860/")

    # driver.get("https://www.selenium.dev/documentation/webdriver/getting_started/first_script/")

    driver.implicitly_wait(10)


    generateBottom = driver.find_element(by=By.ID, value="txt2img_generate")
    generateBottom.click()
    while True:
        pass
    # driver.quit()

test_eight_components()