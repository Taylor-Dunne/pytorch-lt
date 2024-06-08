import time
import sys
import random
import string
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse

def generate_random_name(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
    return driver

def main_loop(num_wanted=100, url="https://plicated18.blog/invite/i=26624"):
    parse_object = urlparse(url)
    check_url = f"https://{parse_object.netloc}/freePreview"
    print(check_url)

    success_count = 0

    for index in range(num_wanted):
        try:
            print("Starting", index)
            driver = get_driver()
            
            driver.get(url)
            time.sleep(5)

            print(driver.current_url)
            print(driver.page_source)

            username_field = driver.find_element(By.NAME, "username")
            password_field = driver.find_element(By.NAME, "password")
            confirm_password_field = driver.find_element(By.NAME, "repeatPassword")

            login = generate_random_name()
            username_field.send_keys(login)
            password_field.send_keys(login)
            confirm_password_field.send_keys(login)

            password_field.send_keys(Keys.RETURN)

            WebDriverWait(driver, 10).until(EC.url_matches(check_url))
            print("Done", driver.current_url)

            success_count += 1

        except Exception as e:
            print(f"Error on attempt {index}: {e}")

        finally:
            driver.quit()

    success_rate = (success_count / num_wanted) * 100
    print(f"Success rate: {success_rate:.2f}% ({success_count}/{num_wanted})")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python test_signup.py <num_tries> <website>")
        sys.exit(1)

    num_tries = int(sys.argv[1])
    website = sys.argv[2]
    main_loop(num_tries, website)
