#!/usr/bin/env python3

import os
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from config import ACCOUNTS, HEADLESS, BOT_IDS
from app import vote
from app.utils import Logger, has_already_voted_all


def main() -> None:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    driver: webdriver.Chrome

    try:
        for account in ACCOUNTS:
            if has_already_voted_all(account.email, BOT_IDS):
                Logger(f"vote ({account.email})").info(f"Currently no bots to vote.")
                continue

            options = Options()
            options.headless = HEADLESS
            caps = DesiredCapabilities().CHROME
            caps["pageLoadStrategy"] = "eager"
            driver = uc.Chrome(options=options, desired_capabilities=caps)

            vote(driver, account.email, account.password)
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
