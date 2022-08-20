import ddddocr
import time
import os
import sys
import secrets
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

__import__('onnxruntime').set_default_logger_severity(3)

with open(os.path.join(os.path.split(__file__)[0], 'secrets.txt'), 'r', encoding='utf-8') as f:
    USERNAME, PASSWORD = (x.strip() for x in f.read().splitlines())

def getTime() -> str:
    return time.strftime('[%Y-%m-%d %H:%M:%S]')

ocr = ddddocr.DdddOcr()

options = webdriver.FirefoxOptions()
options.headless = True
browser = webdriver.Firefox(options=options)
browser.install_addon(os.path.join(os.path.split(__file__)[0], 'webdriver-cleaner'), temporary=True)

try:
    browser.get('https://cas.sysu.edu.cn/cas/login?service=http%3A%2F%2Fjksb.sysu.edu.cn%2Finfoplus%2Fform%2FXNYQSB%2Fstart')

    loginAttempt = 0
    while browser.current_url.startswith('https://cas.sysu.edu.cn/cas/login'):
        loginAttempt += 1
        if loginAttempt > 5:
            raise Exception('Login failed.')
        print(getTime(), 'Login with NetID:', USERNAME, 'Attempt:', loginAttempt)
        browser.find_element(By.ID, 'username').send_keys(USERNAME)
        browser.find_element(By.ID, 'password').send_keys(PASSWORD)
        browser.find_element(By.ID, 'captcha').send_keys(ocr.classification(browser.find_element(By.ID, 'captchaImg').screenshot_as_png))
        browser.find_element(By.CSS_SELECTOR, 'input[type=submit]').click()
    print(getTime(), f'Login success!')

    WebDriverWait(browser, 15).until(expected_conditions.visibility_of_element_located((By.ID, 'title_description')))
    print(getTime(), 'Form ID:', browser.find_element(By.ID, 'title_description').text.removeprefix('流水号:').removeprefix('SN:'))
    WebDriverWait(browser, 15).until(expected_conditions.text_to_be_present_in_element((By.ID, 'title_content'), '学生健康状况申报:温馨提示'))
    WebDriverWait(browser, 15).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, '#form_command_bar > .command_button > .command_button_content:first-child')))
    browser.find_element(By.CSS_SELECTOR, '#form_command_bar > .command_button > .command_button_content:first-child').click()
    WebDriverWait(browser, 15).until(expected_conditions.text_to_be_present_in_element((By.ID, 'title_content'), '学生健康状况申报:健康信息'))
    WebDriverWait(browser, 15).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, '#form_command_bar > .command_button > .command_button_content:first-child')))
    browser.find_element(By.CSS_SELECTOR, '#form_command_bar > .command_button > .command_button_content:first-child').click()
    WebDriverWait(browser, 15).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.overlay.active > .dialog.display .dialog_content')))
    print(getTime(), 'Result:', browser.find_element(By.CSS_SELECTOR, '.overlay.active > .dialog.display .dialog_content').text)
except Exception as ex:
    print(getTime(), type(ex).__name__, str(ex))
    screenshotPath = os.path.join(os.path.split(__file__)[0], 'screenshot', secrets.token_urlsafe(12) + '.png')
    os.makedirs(os.path.split(screenshotPath)[0], exist_ok=True)
    browser.save_screenshot(screenshotPath)
    print(getTime(), 'Screenshot saved:', screenshotPath)
finally:
    browser.quit()