import os
import time
import ctypes
import logging
from typing import Optional
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (
	NoSuchElementException, ElementClickInterceptedException
)
from config import DEBUG

if os.name == "nt":
	kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
	kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


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
	try:
		element.click()
	except ElementClickInterceptedException:
		click(element)


class Logger(logging.Logger):
	def __init__(self, name: str, *, filepath: Optional[str] = None) -> None:
		super().__init__(name)
		formatter = Formatter()
		
		if filepath:
			file_handler = logging.FileHandler(filepath)
			file_handler.setLevel(logging.DEBUG if DEBUG else logging.INFO)
			file_handler.setFormatter(formatter)
			self.addHandler(file_handler)
		
		stream_handler = logging.StreamHandler()
		stream_handler.setLevel(logging.DEBUG if DEBUG else logging.INFO)
		stream_handler.setFormatter(formatter)
		self.addHandler(stream_handler)


class Formatter(logging.Formatter):
	last_record: Optional[logging.LogRecord] = None
	
	def format(self, record: logging.LogRecord) -> str:
		formatter = logging.Formatter(
			"\n\033[91m%(name)s\033[0m\n"
			"[\033[95m%(asctime)s\033[0m \033[93m%(levelname)s\033[0m] %(message)s"
		)
		
		if Formatter.last_record is not None:
			if record.name == Formatter.last_record.name:
				formatter = logging.Formatter(
					"[\033[95m%(asctime)s\033[0m \033[93m%(levelname)s\033[0m] %(message)s"
				)
		
		Formatter.last_record = record
		return formatter.format(record)
