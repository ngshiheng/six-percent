#!/usr/bin/python3
"""
Title: Six Percent
Author: Ng, Jerry Shi Heng
Last modified: 02 Jun 2019
Website: https://github.com/ngshiheng/six-percent/
"""

# --- Modules --- #
import sys
import time
import pytesseract
import cv2
import win32com.client
from tkinter import *
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


# --- Functions --- #
def print_invalid_input():
    print("> Invalid input, please try again!")
    under_score = "-"
    print(under_score * 70)


def print_success_rate(t_success, t_attempt):
    success_rate = (t_success / t_attempt) * 100
    print("SUCCESS RATE: " + "{:.2f}".format(success_rate) + ("%\n"))


def print_datalog(t_success, t_failure):
    t_attempts = t_failure + t_success
    print("Total attempts: " + str(t_attempts))
    print("Total SUCCESSFUL attempts: " + str(t_success))
    print("Total FAILED attempts: " + str(t_failure))


def start():
    print("Welcome to Six Precent - ASNB auto investment bot!\n")

    asnbFund = {
        0: {'fund_name': 'Amanah Saham Malaysia (ASM)', 'element_name': 'submit2_ASM'},
        1: {'fund_name': 'Amanah Saham Malaysia 2 - Wawasan (ASW)', 'element_name': 'submit_ASW'},
        2: {'fund_name': 'Amanah Saham Malaysia 3 (AS1M)', 'element_name': 'submit_AS1M'}
    }
    delay = 10  # seconds

    myUsername = username.get()
    myPassword = password.get()
    myAmount = int(amount.get())
    myFund = fund.get()

    print("List of available funds:")
    for k, v in asnbFund.items():
        print("> " + str(v['fund_name']))

    if myFund in (0, 1, 2):
        selectedFund = asnbFund[myFund].get('element_name')
        print("\nFund selected: " + asnbFund[myFund].get('fund_name') + "\n")

    # start Google Chrome browser
    print("Launching ASNB web page in Google Chrome...\n")
    browser = webdriver.Chrome()

    # browse the login page for myASNB
    browser.get('https://www.myasnb.com.my/uh/uhlogin/auth')
    browser.find_element_by_class_name('btn-login').click()

    # input username
    print("Logging in...\n")
    browser.find_element_by_id('username').send_keys(myUsername)
    browser.find_element_by_id('submit').click()
    time.sleep(2)

    # input password
    WebDriverWait(browser, delay).until(expected_conditions.presence_of_element_located((By.ID, 'j_password_user')))
    browser.find_element_by_id('j_password_user').send_keys(myPassword)
    WebDriverWait(browser, delay).until(expected_conditions.presence_of_element_located((By.ID, 'submit')))
    browser.find_element_by_id('submit').click()
    print("Successfully logged in.\n")

    # maximize browser window
    browser.maximize_window()

    # click 'Produk'
    WebDriverWait(browser, delay).until(expected_conditions.presence_of_element_located((By.LINK_TEXT, 'Produk')))
    browser.find_element_by_link_text('Produk').click()

    # click 'Pelaburan Permulaan/Tambahan'
    WebDriverWait(browser, delay).until(
        expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[1]')))
    browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div[1]').click()

    # select fund for additional investment
    try:
        WebDriverWait(browser, delay).until(expected_conditions.visibility_of_element_located((By.ID, selectedFund)))
        print('Operation Status:\tOPEN\n')
        print('Continue to select investment funds..\n')
        browser.find_element_by_id(selectedFund).click()
        print("Selecting " + asnbFund[myFund].get('fund_name') + "\n")

    except NoSuchElementException:
        print('Operation Status:\tCLOSED\n')
        print(
            'Operating hours are 07:00 AM to 06:00 PM local time, Sunday to Friday and third Saturday of the month, excluding public holidays\n')
        print('Logging out...\n')
        browser.find_element_by_xpath("//*[contains(text(),'LOG KELUAR')]").click()
        print('Successfully logged out.\n')
        browser.close()
        sys.exit()

    # declaration of PEP
    WebDriverWait(browser, delay).until(lambda s: s.find_element_by_id("NEXT").is_displayed())
    browser.find_element_by_id('NEXT').click()

    # check if checkbox element is checked
    browser.find_element_by_xpath('//*[@id="txnform"]/div/div[1]/div[4]/label/p').click()

    # click next button after checking the check box
    WebDriverWait(browser, delay).until(expected_conditions.presence_of_element_located((By.ID, 'btn-unit-fund')))
    browser.find_element_by_id('btn-unit-fund').click()

    # input investment amount
    WebDriverWait(browser, delay).until(expected_conditions.visibility_of_element_located((By.NAME, 'purchaseamount')))
    browser.find_element_by_name('purchaseamount').send_keys(myAmount)
    browser.find_element_by_id('btn-unit-fund').click()

    # starting to loop purchase attempt
    print("Starting purchase loop...\n")
    tesseract_lang = "six-percent-tesseract"  # @ <C:\Program Files (x86)\Tesseract-OCR\tessdata\six-percent-tesseract.traineddata>
    attempt = 0
    success = 0
    failure = 0

    while True:
        try:
            # identify captcha html element
            captcha_element = browser.find_element_by_class_name('realperson-text')

            # snapshot and save captcha 
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

            # data collection
            # processed_captcha = '%s.png' %attempt # 'processed_captcha.png'

            # implementation mode
            processed_captcha = 'processed_captcha.png'

            save_captcha_image = im.save(original_captcha)  # saves new cropped image

            # read original asnb_captcha.png and pre-process it before applying Tesseract OCR
            img = cv2.imread(original_captcha, cv2.IMREAD_GRAYSCALE)

            # apply blur/resize/filter to captcha
            img = cv2.bilateralFilter(img, 9, 75, 75)
            img = cv2.blur(img, (3, 3))
            img = cv2.resize(img, (280, 80))

            # binarize captcha
            (thres, img_bw) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            cv2.imwrite(processed_captcha, img_bw)

            attempt = attempt + 1
            # apply OCR on the processed captcha image
            captcha_image = Image.open(processed_captcha)
            captcha_output = pytesseract.image_to_string(captcha_image, lang=tesseract_lang,
                                                         config="-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 6")
            print("#" + str(attempt) + "\tCAPTCHA: " + str(captcha_output))

            # enter captcha
            browser.find_element_by_xpath('//*[@id="defaultReal"]').send_keys(captcha_output)
            browser.find_element_by_id('btn-unit-fund').click()

            # captcha decode success rate data collection
            try:
                browser.find_element_by_xpath("//*[contains(text(),'Sila isi kod captcha yang sah')]")
                print('\tCaptcha Decode:\tFAILED\n')
                failure = failure + 1
                if attempt % 10 == 0:
                    print_success_rate(success, attempt)
                continue

            except NoSuchElementException:
                print('\tCaptcha Decode:\tSUCCESS\n')
                success = success + 1
                if attempt % 10 == 0:
                    print_success_rate(success, attempt)
                continue

        # will enter exception when captcha element is no longer found
        except NoSuchElementException:
            print("Stopped purchasing loop, please take a look.\n")
            speak = win32com.client.Dispatch("SAPI.SpVoice")
            speak.Speak("Stopped purchasing loop, please take a look.")
            print_datalog(success, failure)
            print_success_rate(success, attempt)
            break


def main():
    # title of the GUI
    asnb.title("Six Percent")

    # labels for username, password and amount
    Label(asnb, text='Username:', font='Consolas 11 bold').grid(row=0, sticky=W)
    Label(asnb, text='Password:', font='Consolas 11 bold').grid(row=1, sticky=W)
    Label(asnb, text='Investment Amount (RM):', font='Consolas 11 bold').grid(row=2, sticky=W)

    # username and password entries
    us = Entry(asnb)
    pw = Entry(asnb, show="*")
    amt = Entry(asnb)
    us.grid(row=0, column=1, sticky=W)
    pw.grid(row=1, column=1, sticky=W)
    amt.grid(row=2, column=1, sticky=W)

    # funds selection
    selection = IntVar()

    def fundChoice():
        print("Fund Selected: %s" % funds[selection.get()])

    funds = [
        ("Amanah Saham Malaysia (ASM)"),
        ("Amanah Saham Malaysia 2 - Wawasan (ASW)"),
        ("Amanah Saham Malaysia 3 (AS1M)")
    ]

    Label(asnb, text="Select a fund:", font='Consolas 10 bold underline').grid(sticky=W, pady=5, row=3, column=0)
    for index, fund in enumerate(funds):
        Radiobutton(asnb,
                    text=fund,
                    pady=0,
                    font='Consolas 8',
                    indicatoron=1,
                    # command = fundChoice,
                    value=index,
                    variable=selection).grid(sticky=W, pady=0, row=index + 4)

    # start & stop buttons
    frame = Frame(asnb).grid()
    Button(frame, text='START', fg='green', font='Consolas 20 bold ', command=start).grid(sticky=W, row=7, column=0)
    Button(frame, text='QUIT', fg='red', font='Consolas 20 bold', command=asnb.quit).grid(sticky=E, row=7, column=1)

    return us, pw, amt, selection


if __name__ == '__main__':
    asnb = Tk()
    username, password, amount, fund = main()
    asnb.mainloop()
    print('Program terminated.')
