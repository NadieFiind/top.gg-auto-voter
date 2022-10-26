from collections import namedtuple

Account = namedtuple("Account", "email password")

DEBUG = True  # If True, extra logging will be printed on the terminal.
HEADLESS = True  # If True, the browser will have no GUI.
ACCOUNTS = (
	Account("your_email@example.com", "your_password"),
)
BOT_IDS = (
	646937666251915264,
)
