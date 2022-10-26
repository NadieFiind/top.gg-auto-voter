from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from app.utils import Logger, find_element, click
from config import BOT_IDS


def vote(driver: webdriver.Chrome, email: str, password: str) -> None:
	driver.get("https://discord.com/login")
	find_element(driver, By.NAME, "email").send_keys(email)
	find_element(driver, By.NAME, "password").send_keys(password)
	click(find_element(driver, By.XPATH, "//button[@type='submit']"))
	
	for bot_id in BOT_IDS:
		Logger(f"vote ({email})").info(
			f"Voting https://top.gg/bot/{bot_id} as {email}."
		)
		driver.get(f"https://top.gg/bot/{bot_id}")
		click(find_element(driver, By.XPATH, "//a[text()='Login']"))
		click(find_element(driver, By.CLASS_NAME, "lookFilled-yCfaCM"))
		
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
		
		click(find_element(
			driver, By.XPATH, "//button[text()='Vote' and not(@disabled)]"
		))
		Logger(f"vote ({email})").info(
			f"https://top.gg/bot/{bot_id} voted successfully."
		)
