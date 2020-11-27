ASNB_FUNDS_DATA = {
    "ASM": {
        "name": "Amanah Saham Malaysia",
        "alt_name": "ASM",
        "is_active": True,
        "elements": {
            "id": "submit_buy_ASM",
            "initial_investment_xpath": "//input[@id='submit_initial_invest_ASM']",
            "additional_investment_xpath": "//*[@id='form1_ASM']/div/button"
        }
    },
    "ASW": {
        "name": "Amanah Saham Malaysia 2 - Wawasan",
        "alt_name": "ASM2",
        "is_active": True,
        "elements": {
            "id": "submit_buy_ASW",
            "initial_investment_xpath": "//input[@id='submit_initial_invest_ASW']",
            "additional_investment_xpath": "//*[@id='form1_ASW']/div/button"
        }
    },
    "AS1M": {
        "name": "Amanah Saham Malaysia 3",
        "alt_name": "ASM3",
        "is_active": True,
        "elements": {
            "id": "submit_buy_AS1M",
            "initial_investment_xpath": "//input[@id='submit_initial_invest_AS1M']",
            "additional_investment_xpath": "//*[@id='form1_AS1M']/div/button"
        }
    }
}

ASNB_LOGIN_URL = "https://www.myasnb.com.my/uhsessionexpired"

CHROME_DRIVER_PATH = "./bin/driver/chromedriver.exe"
