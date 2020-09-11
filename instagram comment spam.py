import random
import time

import toml
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, \
    InvalidArgumentException
from selenium.webdriver.firefox.options import Options

# user inputted variables
number_of_comments = 10
post_link = r""
login_file = toml.load("login.toml")
user = login_file.get("insta_user")
password = login_file.get("insta_pass")
headless = False

# program variables
count = 0
driver = "geckodriver.exe"
options = Options()
if headless:
    options.headless = True
browser = webdriver.Firefox(executable_path=driver, options=options)

# login
browser.get("https://www.instagram.com")
time.sleep(3)
username_box = browser.find_element_by_name("username")
username_box.send_keys(user)
password_box = browser.find_element_by_name("password")
password_box.send_keys(password)
login_button = browser.find_element_by_xpath(
    "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button")
login_button.click()
time.sleep(5)

# comment
try:
    browser.get(post_link)
    comment_box = browser.find_element_by_xpath(
        "/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[3]/div/form/textarea")
    comment_box.click()
    post_button = browser.find_element_by_xpath(
        "/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[3]/div/form/button")
    while count < number_of_comments:
        try:
            comment = f""
            comment_box = browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[3]/div/form/textarea")
            comment_box.click()
            comment_box.send_keys(comment)
            post_button.click()
            count += 1
            print(f'{count} comments sent')
            time.sleep(random.randint(2, 8))
        except ElementClickInterceptedException:
            print("Delay too low")
            exit()
except NoSuchElementException or InvalidArgumentException:
    print("Private Account you are not following or invalid link")
browser.close()
print(f"{count} comments were sent")
