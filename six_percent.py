#!/usr/bin/python3
"""
Title: Six Percent
Author: Ng, Jerry Shi Heng
Last modified: 19 Aug 2019
Website: https://github.com/ngshiheng/six-percent/
"""

import time, pytesseract, cv2, win32com.client, sys
from PIL import Image
from io import BytesIO
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from asnbfunds import *

INVALID_INPUT_ERROR = "** Invalid input, please try again **"
DELAY = 10

if __name__ == "__main__":
    print("Welcome to ASNB Auto Investment Bot!\n")

    # User input - log in details
    while True:
        username = input("Enter your ASNB user ID:\n> ")
        if not username.strip(' '):
            continue

        else:
            break

    password = getpass("\nEnter your ASNB user PASSWORD:\n> ")

    # User input - investment amount
    investment_amount = 0
    while True:
        try:
            investment_amount = int(input("\nEnter your investment amount in RM (minimum RM100):\n> "))
            if investment_amount >= 100:
                break
            else:
                raise ValueError
        except ValueError:
            print(INVALID_INPUT_ERROR)
            continue

    # User input - fund choice
    fixed_price_funds = {
        1: 'Amanah Saham Malaysia (ASM)',
        2: 'Amanah Saham Malaysia 2 - Wawasan (ASW)',
        3: 'Amanah Saham Malaysia 3 (AS1M)',
    }

    print("\nEnter choose a fixed price fund to invest in:\n")
    for choice, fund in fixed_price_funds.items():
        print(f"> {choice}. {fund}")

    selected_fund = None
    while True:
        try:
            choices = int(input("> "))
            if choices == 1:
                selected_fund = AmanahSahamMalaysia()
                break

            elif choices == 2:
                selected_fund = AmanahSahamMalaysia2()
                break

            elif choices == 3:
                selected_fund = AmanahSahamMalaysia3()
                break

            else:
                raise ValueError

        except ValueError:
            print(INVALID_INPUT_ERROR)
            continue
    print("\n")
    print(f"Fund selected: {selected_fund.name}")

    # Start browser
    print("Launching ASNB web page in Google Chrome...\n")
    browser = webdriver.Chrome()
    browser.implicitly_wait(DELAY)  # seconds
    browser.get('https://www.myasnb.com.my/uh/uhlogin/auth')
    browser.find_element_by_class_name('btn-login').click()

    # Enter log in details
    print("Logging in...")
    browser.find_element_by_id('username').send_keys(username)
    browser.find_element_by_id('username').send_keys(Keys.ENTER)

    browser.find_element_by_id('j_password_user').send_keys(password)
    browser.find_element_by_id('j_password_user').send_keys(Keys.ENTER)
    print("Successfully logged in.")

    # Maximize browser
    browser.maximize_window()

    # Click 'Produk'
    browser.find_element_by_link_text('Produk').click()

    # Click 'Transaksi'
    browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div[1]').click()

    # Drop down and select fund
    browser.find_element_by_xpath(selected_fund.transaction_drop_down_xpath_name).click()
    print('Operation Status:\tOPEN')
    print('Continue to select investment funds..')
    browser.find_element_by_id(selected_fund.additional_investment_element_name).click()

    # Declaration of PEP
    WebDriverWait(browser, DELAY).until(lambda s: s.find_element_by_id("NEXT").is_displayed())
    browser.find_element_by_id('NEXT').click()

    # Terms and agreement checkbox
    start_time = time.time()
    while True:
        try:
            browser.find_element_by_xpath('//*[@id="txnform"]/div/div[1]/div[4]/label/p').click()
            break

        except WebDriverException as e:
            if time.time() - start_time > DELAY:
                raise e
            time.sleep(0.5)

    # Click next button after checking the check box
    browser.find_element_by_id('btn-unit-fund').click()

    # Input investment amount
    browser.find_element_by_name('purchaseamount').send_keys(investment_amount)
    browser.find_element_by_name('purchaseamount').send_keys(Keys.ENTER)

    # Starting to loop purchase attempt
    print("Starting purchase loop...\n")
    tesseract_lang = "six-percent-tesseract"  # @ <C:\Program Files (x86)\Tesseract-OCR\tessdata\six-percent-tesseract.traineddata>
    attempt = 0

    while True:
        try:
            # Identify captcha html element
            captcha_element = browser.find_element_by_class_name('realperson-text')

            # Snapshot and save captcha
            location = captcha_element.location
            size = captcha_element.size
            png = browser.get_screenshot_as_png()
            left = location['x'] - 5
            top = location['y'] - 5
            right = location['x'] + 145  # size['width']
            bottom = location['y'] + size['height'] + 5

            im = Image.open(BytesIO(png))
            im = im.crop((left, top, right, bottom))  # defines crop points

            original_captcha = 'original_captcha' + '.png'

            # Data collection
            # processed_captcha = '%s.png' %attempt # 'processed_captcha.png'

            # Implementation mode
            processed_captcha = 'processed_captcha.png'
            save_captcha_image = im.save(original_captcha)  # saves new cropped image

            # Read original asnb_captcha.png and pre-process it before applying Tesseract OCR
            img = cv2.imread(original_captcha, cv2.IMREAD_GRAYSCALE)

            # Apply blur/resize/filter to captcha
            img = cv2.bilateralFilter(img, 9, 75, 75)
            img = cv2.blur(img, (3, 3))
            img = cv2.resize(img, (280, 80))

            # Binarize captcha
            (thres, img_bw) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            cv2.imwrite(processed_captcha, img_bw)

            # Apply OCR on the processed captcha image
            attempt = attempt + 1
            captcha_image = Image.open(processed_captcha)
            captcha_output = pytesseract.image_to_string(
                captcha_image,
                lang=tesseract_lang,
                config="-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 6"
            )
            print("#" + str(attempt) + "\tCAPTCHA: " + str(captcha_output))

            # Enter captcha
            browser.find_element_by_xpath('//*[@id="defaultReal"]').send_keys(captcha_output)
            browser.find_element_by_xpath('//*[@id="defaultReal"]').send_keys(Keys.ENTER)
            continue

        # Will enter exception when captcha element is no longer found
        except:
            print("\nStopped purchasing loop, please take a look.\n")
            speak = win32com.client.Dispatch("SAPI.SpVoice")
            speak.Speak("Stopped purchasing loop, please take a look.")
            print("Total attempts: " + str(attempt))
            print("Please remember to logout before you exit the terminal")
            break
    sys.exit()
