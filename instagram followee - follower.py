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
    browser.get("https://www.instagram.com/" + user)
    following_number = browser.find_element_by_css_selector("li.Y8-fY:nth-child(3) > a:nth-child(1)").text
    time.sleep(2)
    browser.find_element_by_partial_link_text('following').click()
    time.sleep(5)
    return following_number


def open_followers(user):
    browser.get("https://instagram.com/" + user)
    followers_number = browser.find_element_by_css_selector("li.Y8-fY:nth-child(2) > a:nth-child(1)").text
    time.sleep(2)
    browser.find_element_by_partial_link_text('followers').click()
    time.sleep(5)
    return followers_number


def scroll(number):
    browser.find_element_by_class_name("PZuss").click()
    for _ in range(math.ceil(number / 11)):
        browser.find_element_by_css_selector("body").send_keys(Keys.CONTROL, Keys.END)
        time.sleep(1)


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
print("Logged in")


def main():
    # get following list
    number_of_following = str(open_following(username).replace(" following", ""))
    scroll(int(number_of_following))
    following_list = browser.find_elements_by_class_name("wo9IH")
    following_list = convert_list_into_text(following_list)
    print("Scraped following")

    # get followers list
    number_of_followers = str(open_followers(username).replace(" followers", ""))
    scroll(int(number_of_followers))
    followers_list = browser.find_elements_by_class_name("wo9IH")
    followers_list = convert_list_into_text(followers_list)
    print("Scraped followers")

    browser.quit()
    acceptable = set()
    diff = set(following_list) - set(followers_list)
    print(diff - acceptable)


if __name__ == '__main__':
    main()
