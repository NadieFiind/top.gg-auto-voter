import os
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from app.utils import Logger, find_element, click
from config import BOT_IDS


def _has_already_voted(email: str, bot_id: int) -> bool:
    if not os.path.isfile("data.json"):
        with open("data.json", "w") as fp:
            json.dump({}, fp)

        return False

    with open("data.json", "r") as fp:
        data = json.load(fp)

        user = data.get(email)
        if user is None:
            return False

        last_voted = user["last_votes"].get(str(bot_id))
        if last_voted is None:
            return False

        dt_now = datetime.now()
        dt_last = datetime.fromisoformat(last_voted)
        difference = (dt_now - dt_last).total_seconds()
        if difference >= 60 * 60 * 12:
            return False

        return True


def _update_vote_data(email: str, bot_id: int) -> None:
    with open("data.json", "r") as fp:
        data = json.load(fp)
        user = data.get(email) or {"last_votes": {}}
        user["last_votes"][str(bot_id)] = datetime.now().isoformat()
        data[email] = user

    with open("data.json", "w") as fp:
        json.dump(data, fp, indent="    ")


def vote(driver: webdriver.Chrome, email: str, password: str) -> None:
    driver.get("https://discord.com/login")
    find_element(driver, By.NAME, "email").send_keys(email)
    find_element(driver, By.NAME, "password").send_keys(password)
    click(find_element(driver, By.XPATH, "//button[@type='submit']"))

    for index, bot_id in enumerate(BOT_IDS):
        Logger(f"vote ({email})").info(f"Voting https://top.gg/bot/{bot_id}.")

        driver.get(f"https://top.gg/bot/{bot_id}")

        if index == 0:
            click(find_element(driver, By.XPATH, "//a[text()='Login']"))
            click(find_element(driver, By.CLASS_NAME, "lookFilled-yCfaCM"))

        if _has_already_voted(email, bot_id):
            Logger(f"vote ({email})").info(
                f"https://top.gg/bot/{bot_id} already voted. Skipped."
            )
            continue

        try:
            click(find_element(driver, By.XPATH, f"//a[@href='/bot/{bot_id}/vote']"))
        except NoSuchElementException:
            Logger(f"vote ({email})").info(
                "Discord log in unsuccessful.\n\n"
                "Possible Reasons:\n"
                "  - You have invalid account credentials in the config.ACCOUNTS.\n"
                "  - A CAPTCHA blocked the log in process.\n\n"
                "If the latter, please log in manually to verify your account. "
                "After logging in, restart the application. "
                "If you cannot see the browser, set the config.HEADLESS to False "
                "and run the application again."
            )
            while True:
                pass

        click(
            find_element(driver, By.XPATH, "//button[text()='Vote' and not(@disabled)]")
        )

        _update_vote_data(email, bot_id)
        Logger(f"vote ({email})").info(
            f"https://top.gg/bot/{bot_id} voted successfully."
        )
