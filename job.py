#!/usr/bin/env python3

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import undetected_chromedriver as uc
from config import ACCOUNTS, HEADLESS
from app import vote
from app.utils import Logger


def main() -> None:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    driver: webdriver.Chrome

    try:
        for account in ACCOUNTS:
            options = Options()
            options.headless = HEADLESS
            caps = DesiredCapabilities().CHROME
            caps["pageLoadStrategy"] = "eager"
            driver = uc.Chrome(options=options, desired_capabilities=caps)

            vote(driver, account.email, account.password)
            time.sleep(3)
            driver.quit()
    except KeyboardInterrupt:
        pass
    except Exception:
        Logger("job").exception("An error occurred while voting.")
    finally:
        try:
            driver.quit()
        except NameError:
            pass


if __name__ == "__main__":
    main()
