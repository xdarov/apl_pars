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
    count = 0

    @classmethod
    def authorization(cls, driver):
        email = driver.find_element(By.XPATH, '//*[@id="email"]')
        email.send_keys(config.email)
        password = driver.find_element(By.XPATH, '//*[@id="password"]')
        password.send_keys(config.password)
        button = driver.find_element(
            By.XPATH, '/html/body/div/div[2]/div/div/form/div[3]/button[1]')
        button.click()

    @classmethod
    def check_shop(cls, driver):
        sleep(7)
        check_new = driver.find_element(By.CLASS_NAME, 'shop-list') \
            .find_elements(By.CLASS_NAME, 'react-multi-carousel-item')
        print(len(check_new))
        if cls.count == 0:
            cls.count = len(check_new)
            telebot.TeleBot(config.TOKEN).send_message(
                config.CHAT_ID[0], f'CHECK VALUE IS {cls.count}')
        if (len(check_new) := len_check_new) != cls.count and len_check_new != 0:
            cls.count = len(check_new)
            print(f'CHECK APLICANT!!! {cls.count}')
            for id in config.CHAT_ID:
                telebot.TeleBot(config.TOKEN).send_message(
                    id, f'CHECK APLICANT!!! {cls.count}')

    @classmethod
    def pars_run(cls):
        while True:
            try:
                options = Options()
                options.set_preference(
                    "general.useragent.override", config.user_agent)
                driver = Firefox(options=options)
                driver.set_page_load_timeout(7)
                driver.get('https://applicant.21-school.ru/shop')
                sleep(5)
                cls.authorization(driver)
                restart = 0
                while True:
                    try:
                        sleep(10)
                        driver.refresh()
                        cls.check_shop(driver)
                        restart += 1
                        if restart >= 10:
                            raise StopIteration('Restart')
                    except (NoSuchElementException, TimeoutException) as e:
                        print(f'-->ERROR<-- {e}')
            except StopIteration:
                pass
            except Exception as e:
                print(f'-->ERROR<-- {e}')
                os.system(
                    f"echo '{datetime.now()} -->ERROR<-- {e}' >> LOG.txt")
            finally:
                try:
                    driver.close()
                except NoSuchWindowException:
                    pass


if __name__ == '__main__':
    AplicantShop.pars_run()
