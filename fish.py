#coding=utf-8

import os
import time
import random
import string
import base64
from selenium import webdriver

nums = 10
# imgcat命令绝对路径
imgcat = '/usr/local/bin/imgcat'
path = os.path.abspath(__file__)

# 验证码图片存放路径
image_path = os.path.join(os.path.dirname(path), 'test.jpg')

options = webdriver.ChromeOptions()

# 设置代理
options.add_argument('--proxy-server=http://127.0.0.1:1087')

driver = webdriver.Chrome(options=options)

# 定义模拟邀请的人数
for i in range(0, nums):
    driver.get('http://www.yopmail.com/zh/email-generator.php')
    time.sleep(1)
    email = driver.find_element_by_id("login")
    email = email.get_attribute('value')

	# 打开邀请注册的链接
    driver.get('http://my.fishbank.io/go/122169')
    time.sleep(1)
    login_btn = driver.find_element_by_css_selector('.button.red.bigrounded.big')
    login_btn.click()
    driver.get('https://my.fishbank.io/register')
    time.sleep(1)
    email_input = driver.find_element_by_id('user_email')
    password_one = driver.find_element_by_id('user_plainPassword_first')
    password_two = driver.find_element_by_id('user_plainPassword_second')
    cap_input = driver.find_element_by_id('user_captcha')
    register_btn = driver.find_element_by_css_selector('.button.green.bigrounded.mid')

    cap = driver.find_element_by_class_name('captcha_image')
    with open(image_path, 'wb') as fi:
        fi.write(base64.b64decode(cap.get_attribute('src').split(',')[1]))
    os.system(imgcat+' '+image_path)
    code = input('输入验证码')

    password = ''.join(random.sample(string.ascii_letters+string.digits, 10))
    email_input.send_keys(email)
    password_one.send_keys(password)
    password_two.send_keys(password)
    cap_input.send_keys(code)
    time.sleep(2)
    register_btn.click()

    time.sleep(1)
    driver.get('http://www.yopmail.com/zh/')
    time.sleep(1)
    email_input = driver.find_element_by_id('login')
    check_btn = driver.find_element_by_class_name('sbut')
    email_input.send_keys(email)
    check_btn.click()
    driver.switch_to_frame(driver.find_element_by_id('ifmail'))
    try:
        html = driver.find_element_by_id('mailmillieu')
    except Exception as e:
        input('遇到机器识别的问题，切换到浏览器点击一下，验证完敲一下回车')
        html = driver.find_element_by_id('mailmillieu')
    html = html.text
    active_url = html.split('account:')[1].strip()
    driver.get(active_url)
    time.sleep(1)
    driver.delete_all_cookies()
    time.sleep(1)
driver.close()

