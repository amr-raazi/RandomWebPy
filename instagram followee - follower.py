import toml
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import math
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.firefox.options import Options

# program variables
driver_path = "geckodriver.exe"
options = Options()
options.headless = True
browser = webdriver.Firefox(executable_path=driver_path, options=options)

# user variables
login_file = toml.load("login.toml")
login_user = login_file.get("insta_user")
login_pass = login_file.get("insta_pass")
username = ""


def login(driver, login_username, login_password):
    driver.get("https://www.instagram.com")
    time.sleep(3)
    username_box = browser.find_element_by_name("username")
    username_box.send_keys(login_username)
    password_box = browser.find_element_by_name("password")
    password_box.send_keys(login_password)
    login_button = browser.find_element_by_xpath(
        "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button")
    login_button.click()
    time.sleep(5)


def open_following(user):
    user_link = "https:\\instagram.com/" + user
    browser.get(user_link)
    following_number = browser.find_element_by_css_selector("li.Y8-fY:nth-child(3) > a:nth-child(1)").text
    time.sleep(2)
    following_button = browser.find_element_by_partial_link_text('following')
    following_button.click()
    time.sleep(5)
    return following_number


def open_followers(user):
    user_link = "https:\\instagram.com/" + user
    browser.get(user_link)
    followers_number = browser.find_element_by_css_selector("li.Y8-fY:nth-child(2) > a:nth-child(1)").text
    time.sleep(2)
    followers_button = browser.find_element_by_partial_link_text('followers')
    followers_button.click()
    time.sleep(5)
    return followers_number


def scroll(number):
    browser.find_element_by_class_name("_1XyCr").click()
    for i in range(math.ceil(number / 11)):
        browser.find_element_by_css_selector("body").send_keys(Keys.CONTROL, Keys.END)
        time.sleep(4)


def convert_list_into_text(selenium_list):
    out = []
    for element in selenium_list:
        try:
            element = element.text
            element = element.splitlines()
            element = element[0]
            out.append(element)
        except StaleElementReferenceException:
            continue
    return out


# login
login(browser, login_user, login_pass)

# get following list
number_of_following = int(open_following(username).replace(" following", ""))
scroll(number_of_following)
following_list = browser.find_elements_by_class_name("wo9IH")
following_list = convert_list_into_text(following_list)

# get followers list
number_of_followers = int(open_followers(username).replace(" followers", ""))
scroll(number_of_followers)
followers_list = browser.find_elements_by_class_name("wo9IH")
followers_list = convert_list_into_text(followers_list)

browser.quit()

# check differences
differences = []
for following in following_list:
    if following not in followers_list:
        differences.append(following)
print(differences)
