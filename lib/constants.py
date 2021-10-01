# General
ASNB_LOGIN_URL = "https://www.myasnb.com.my/login"
CHROME_DRIVER_PATH = "./bin/driver/chromedriver.exe"

TOTAL_FUND_COUNT = 3
MAX_PURCHASE_RETRY_ATTEMPTS = 10

# Time settings
ASNB_COOLDOWN_PERIOD = 5  # minutes per fund
TIMEOUT_LIMIT = 10  # seconds
PAYMENT_TIMEOUT_LIMIT = 300  # seconds


# XPATHs

# https://www.myasnb.com.my/portfolio
ENGLISH_LANGUAGE_BUTTON_XPATH = "//a[@name='en']"
FUNDS_XPATH = "//div[@class='justify-between hidden md:block text-xs lg:text-sm']"
ERROR_PROMPT_OK_BUTTON_XPATH = "//button[contains(@class, 'text-white') and @type='submit']"


# https://www.myasnb.com.my/transactions
INVESTMENT_AMOUNT_XPATH = "//input[@name='amount']"
BANK_DROPDOWN_SELECTION_XPATH = "//select[@name='banks']/option[@value='Maybank2U']"
TERMS_AND_CONDITIONS_CHECKBOX_XPATH = "//input[@type='checkbox']"

PEP_DECLARATION_PROMPT_XPATH = "//h3[contains(text(), 'Declaration of PEP')]"
PEP_DECLARATION_PROMPT_NEXT_BUTTON_XPATH = "//button[contains(text(), 'Next')]"
SUBMIT_BUTTON_XPATH = "//button[@type='submit']"

PROMPT_OK_BUTTON_XPATH = "//button[contains(@class, 'text-white') and @type='button']"
PORTFOLIO_URL_XPATH = "//a[@href='/portfolio']"
