from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, \
    TimeoutException, NoSuchWindowException
from datetime import datetime
from time import sleep
import telebot
import config
import os

class AplicantShop:

    @classmethod
    def authorization(cls, driver):
        email = driver.find_element(By.XPATH, '//*[@id="email"]')
        email.send_keys(config.email)
        password = driver.find_element(By.XPATH, '//*[@id="password"]')
        password.send_keys(config.password)
        button = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div/form/div[3]/button[1]')
        button.click()

    @classmethod
    def check_shop(cls, driver):
        sleep(7)
        check_new = driver.find_element(By.CLASS_NAME, 'shop-list') \
            .find_elements(By.CLASS_NAME, 'react-multi-carousel-item')
        if len(check_new) > 61:
            print(f'CHECK APLICANT!!! {len(check_new)}')
            telebot.TeleBot(config.TOKEN).send_message(config.CHAT_ID, f'CHECK APLICANT!!! {len(check_new)}')


    @classmethod
    def pars_run(cls):
        
        while True:
            try:
                options = Options()
                options.set_preference("general.useragent.override", config.user_agent)
                driver = Firefox(options=options)
                driver.set_page_load_timeout(7)
                driver.get('https://applicant.21-school.ru/shop')
                sleep(5)
                cls.authorization(driver)
                while True:
                    try:
                        sleep(10)
                        driver.refresh()
                        cls.check_shop(driver)
                    except (NoSuchElementException, TimeoutException) as e:
                        print(f'-->ERROR<-- {e}')
            except Exception as e:
                print(f'-->ERROR<-- {e}')
                os.system(f"echo '{datetime.now()} -->ERROR<-- {e}' >> LOG.txt")
            finally:
                try:
                    driver.close()
                except NoSuchWindowException:
                    pass

if __name__ == '__main__':
     
    AplicantShop.pars_run()
