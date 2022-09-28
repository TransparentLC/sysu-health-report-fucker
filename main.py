import ddddocr
import time
import os
import secrets
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

__import__('onnxruntime').set_default_logger_severity(3)

with open(os.path.join(os.path.dirname(__file__), 'secrets.txt'), 'r', encoding='utf-8') as f:
    USERNAME, PASSWORD = (x.strip() for x in f.read().splitlines())

def getTime() -> str:
    return time.strftime('[%Y-%m-%d %H:%M:%S]')

if 'show_ad' in ddddocr.DdddOcr.__init__.__code__.co_varnames:
    ocr = ddddocr.DdddOcr(show_ad=False)
else:
    ocr = ddddocr.DdddOcr()

options = webdriver.FirefoxOptions()
options.headless = True
browser = webdriver.Firefox(options=options)
browser.install_addon(os.path.join(os.path.dirname(__file__), 'webdriver-cleaner'), temporary=True)
browser.install_addon(os.path.join(os.path.dirname(__file__), 'request-blocker'), temporary=True)

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

    WebDriverWait(browser, 15).until(expected_conditions.visibility_of_element_located((By.ID, 'title_description_short')))
    print(getTime(), 'Form ID:', browser.find_element(By.ID, 'title_description_short').text.removeprefix('流水号:').removeprefix('SN:'))
    WebDriverWait(browser, 15).until(expected_conditions.text_to_be_present_in_element((By.ID, 'title_content'), '学生健康状况申报:温馨提示'))
    WebDriverWait(browser, 15).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, '#form_command_bar > .command_button > .command_button_content:first-child')))
    browser.find_element(By.CSS_SELECTOR, '#form_command_bar > .command_button > .command_button_content:first-child').click()
    WebDriverWait(browser, 15).until(expected_conditions.text_to_be_present_in_element((By.ID, 'title_content'), '学生健康状况申报:健康信息'))
    WebDriverWait(browser, 15).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, '#form_command_bar > .command_button > .command_button_content:first-child')))
    try:
        if not browser.find_element(By.CSS_SELECTOR, 'input[name="fieldSQgzszx"]').is_selected():
            browser.find_element(By.CSS_SELECTOR, 'input[name="fieldSQgzszx"]').click()
    except NoSuchElementException:
        pass
    browser.find_element(By.CSS_SELECTOR, '#form_command_bar > .command_button > .command_button_content:first-child').click()
    WebDriverWait(browser, 15).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.overlay.active > .dialog.display .dialog_content')))
    resultText = browser.find_element(By.CSS_SELECTOR, '.overlay.active > .dialog.display .dialog_content').text
    if resultText not in {
        'Done successfully!',
        '办理成功!',
    }:
        raise Exception(f'Result: {resultText}')
    print(getTime(), 'Health report success!')
    browser.quit()
except Exception as ex:
    print(getTime(), type(ex).__name__, str(ex))
    screenshotPath = os.path.join(os.path.dirname(__file__), 'screenshot', secrets.token_urlsafe(12) + '.png')
    os.makedirs(os.path.dirname(screenshotPath), exist_ok=True)
    browser.save_screenshot(screenshotPath)
    print(getTime(), 'Screenshot saved:', screenshotPath)
    browser.quit()
    sys.exit(1)
