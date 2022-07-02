from selenium.webdriver.common.by import By


class LoginPageLocators:
    """www.myasnb.com.my/login"""

    USERNAME = (By.XPATH, "//input[@name='username']")
    SECURITY_PHRASE_CONFIRMATION = (By.XPATH, "//button[@id='btnYes']")  # "Adakah ini frasa keselamatan anda?"
    PASSWORD = (By.XPATH, "//input[@name='password']")


class PortfolioPageLocators:
    """www.myasnb.com.my/portfolio"""

    FUNDS = (By.XPATH, "//a[@class='hidden xl:block']//*[name()='svg' and @class='h-8 w-8 text-brand hidden xl:block cursor-pointer']")
    ERROR_PROMPT_OK_BUTTON = (By.XPATH, "//button[contains(@class, 'text-white') and @type='submit']")

    LOGOUT_BUTTON = (By.LINK_TEXT, "LOG KELUAR")
    LOGOUT_CONFIRMATION_MESSAGE = (By.XPATH, "//span[contains(text(), 'Berjaya Log Keluar')]")


class TransactionPageLocators:
    """www.myasnb.com.my/transactions"""

    INVESTMENT_AMOUNT = (By.XPATH, "//input[@name='amount']")
    BANK_DROPDOWN_SELECTION = (By.XPATH, "//select[@name='banks']/option[@value='Maybank2U']")
    TERMS_AND_CONDITIONS_CHECKBOX = (By.XPATH, "//input[@type='checkbox']")

    PEP_DECLARATION_PROMPT = (By.XPATH, "//h3[contains(text(), 'Pengisytiharan PEP')]")
    PEP_DECLARATION_PROMPT_NEXT_BUTTON = (By.XPATH, "//*[contains(text(), 'Seterusnya')]")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")

    PROMPT_OK_BUTTON = (By.XPATH, "//button[contains(@class, 'text-white') and @type='button']")
    MY_ACCOUNT = (By.XPATH, "//span[contains(text(), 'Akaun Saya')]")
