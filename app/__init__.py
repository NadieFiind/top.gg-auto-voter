from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from app.utils import Logger, find_element
from config import BOT_IDS


def vote(driver: webdriver.Chrome, email: str, password: str) -> None:
	driver.get("https://discord.com/login")
	find_element(driver, By.NAME, "email").send_keys(email)
	find_element(driver, By.NAME, "password").send_keys(password)
	find_element(driver, By.XPATH, "//button[@type='submit']").click()
	
	for bot_id in BOT_IDS:
		Logger("vote").info(f"Voting bot {bot_id} as {email}.")
		driver.get(f"https://top.gg/bot/{bot_id}")
		find_element(driver, By.XPATH, "//a[text()='Login']").click()
		find_element(driver, By.CLASS_NAME, "lookFilled-yCfaCM").click()
		
		try:
			find_element(driver, By.XPATH, f"//a[@href='/bot/{bot_id}/vote']").click()
		except NoSuchElementException:
			Logger("vote").info(
				"Please log in manually to verify your account. "
				"After logging in, restart the application. "
				"If you cannot see the browser, set the config.HEADLESS to False."
			)
			while True:
				pass
		
		find_element(
			driver, By.XPATH, "//button[text()='Vote' and not(@disabled)]"
		).click()
		Logger("vote").info(f"Bot {bot_id} voted successfully.")
