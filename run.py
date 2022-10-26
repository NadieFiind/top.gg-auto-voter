def _vote() -> None:
	global driver
	
	for account in ACCOUNTS:
		options = Options()
		options.headless = HEADLESS
		options.add_argument(  # type: ignore[no-untyped-call]
			"user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
			"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'"
		)
		caps = DesiredCapabilities().CHROME
		caps["pageLoadStrategy"] = "eager"
		driver = webdriver.Chrome(options=options, desired_capabilities=caps)
		
		vote(driver, account.email, account.password)
		time.sleep(3)
		driver.close()
	
	scheduler.enter(60 * 60 * 12, 1, _vote)
	Logger("vote").info(
		"Voting will start again in 12 hours. Please don't exit the application."
	)


if __name__ == "__main__":
	import time
	import sched
	import logging
	from selenium import webdriver
	from selenium.webdriver.chrome.options import Options
	from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
	import chromedriver_autoinstaller  # type: ignore[import]
	from config import ACCOUNTS, HEADLESS
	from app import vote
	from app.utils import Logger
	
	chromedriver_autoinstaller.install()
	logging.getLogger(
		"selenium.webdriver.remote.remote_connection"
	).setLevel(logging.WARNING)
	
	driver: webdriver.Chrome
	scheduler = sched.scheduler(time.time, time.sleep)
	
	try:
		_vote()
		scheduler.run()
		driver.quit()
	except KeyboardInterrupt:
		pass
