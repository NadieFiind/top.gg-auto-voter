import os
import json
import time
import ctypes
import logging
from datetime import datetime
from typing import Optional, List
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
)
from config import DEBUG

if os.name == "nt":
    kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


def has_already_voted(email: str, bot_id: int) -> bool:
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


def has_already_voted_all(email: str, bot_ids: List[int]) -> bool:
    for bot_id in bot_ids:
        voted = has_already_voted(email, bot_id)

        if not voted:
            return False

    return True


def find_element(
    driver: webdriver.Chrome, by: str, value: str, *, retries: int = 30
) -> WebElement:
    Logger("find_element").debug(f"{by}: {value}")

    try:
        return driver.find_element(by=by, value=value)
    except NoSuchElementException as e:
        if retries <= 0:
            raise e

        time.sleep(1)
        return find_element(driver, by, value, retries=retries - 1)


def click(element: WebElement) -> None:
    Logger("click").debug(element)

    try:
        element.click()
        time.sleep(1)
    except ElementClickInterceptedException:
        click(element)


class Logger(logging.Logger):
    def __init__(self, name: str) -> None:
        super().__init__(name)

        file_handler = logging.FileHandler("log.txt")
        file_handler.setLevel(logging.DEBUG if DEBUG else logging.INFO)
        file_handler.setFormatter(Formatter(colored=False))
        self.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG if DEBUG else logging.INFO)
        stream_handler.setFormatter(Formatter())
        self.addHandler(stream_handler)


class Formatter(logging.Formatter):
    last_record: Optional[logging.LogRecord] = None

    def __init__(self, *, colored: bool = True) -> None:
        self.colored = colored

    def format(self, record: logging.LogRecord) -> str:
        if self.colored:
            formatter = logging.Formatter(
                "\n\033[91m%(name)s\033[0m\n"
                "[\033[95m%(asctime)s\033[0m \033[93m%(levelname)s\033[0m] %(message)s"
            )
        else:
            formatter = logging.Formatter(
                "\n%(name)s\n" "[%(asctime)s %(levelname)s] %(message)s"
            )

        if Formatter.last_record is not None:
            if record.name == Formatter.last_record.name:
                if self.colored:
                    formatter = logging.Formatter(
                        "[\033[95m%(asctime)s\033[0m \033[93m%(levelname)s\033[0m] %(message)s"
                    )
                else:
                    formatter = logging.Formatter(
                        "[%(asctime)s %(levelname)s] %(message)s"
                    )

        if self.colored:
            Formatter.last_record = record

        return formatter.format(record)
