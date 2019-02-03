'''
library requirement:

- sys
- time
- selenium
- pytesseract
- cv2
- win32com.client
- PIL
- io
'''

# --- Modules --- #
import sys, time, pytesseract, cv2, win32com.client
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

def printInvalidInput():
    print("> Error, please try again.")
    under_score = "-"
    print(under_score * 70)

def printSuccessRate(t_success, t_attempt):
    success_rate = (t_success/t_attempt)*100
    print("SUCCESS RATE: " + "{:.2f}".format(success_rate) + ("%\n"))
    

def printDatalog(t_success, t_failure):
    t_attempts = t_failure + t_success
    print("Total attempts: " + str(t_attempts) + "\n")
    print("Total SUCCESSFUL attempts: " + str(t_success) + "\n")
    print("Total FAILED attempts: " + str(t_failure) + "\n") 


# --- Accounts --- #
userAccount = {'alan' : {'asnb_username': 'useralan', 'asnb_password': 'alanspassword'},
               'bob' : {'asnb_username': 'userbob', 'asnb_password': 'bobspassword'},
               'charles' : {'asnb_username': 'usercharles', 'asnb_password': 'charlespassword'}}

# --- List of fixed price fund --- #
asnbFund = {1: {'fund_name':'Amanah Saham Malaysia (ASM)', 'element_name':'submit2_ASM'},
            2: {'fund_name':'Amanah Saham Malaysia 2 - Wawasan (ASW)', 'element_name':'submit_ASW'},
            3: {'fund_name':'Amanah Saham Malaysia 3 (AS1M)', 'element_name':'submit_AS1M'}}

# --- Start of program --- #

if __name__ == "__main__":
    delay = 10 # seconds
    print("Welcome to ASNB Auto Investment Bot!\n")

    # select user
    while True:
        myUser = input("Please identify yourself:\n")
        if myUser in userAccount:
            print("Greetings, " + myUser.title() + "!\n")
            myUsername = userAccount[myUser].get('asnb_username')
            myPassword = userAccount[myUser].get('asnb_password')
            break
        else:
            printInvalidInput()
            continue

    # enter investment amount
    while True:
        try:
            myAmount = int(input("Enter your investment amount in RM (minimum RM100):\n"))
            if myAmount >= 100:
                break
            else:
                raise ValueError
        except:
            printInvalidInput()
            continue

    # select fund to invest
    print("\nEnter your fixed price fund to invest in:")
    for k,v in asnbFund.items():
        print("> " + str(k) + " " + str(v['fund_name']))

    while True:
        try:            
            myFund = int(input())
            if myFund in (1,2,3):
                selectedFund = asnbFund[myFund].get('element_name')
                print("Fund selected: " + asnbFund[myFund].get('fund_name') + "\n")
                break
            
            else:
                raise ValueError
        except:
            printInvalidInput()
            continue

    # start Google Chrome browser
    print("Launching ASNB web page in Google Chrome...\n")
    browser = webdriver.Chrome()
    browser.get('https://www.myasnb.com.my/uh/uhlogin/auth')

    browser.find_element_by_class_name('btn-login').click()



    # input username
    print("Logging in...\n")
    browser.find_element_by_id('username').send_keys(myUsername)
    browser.find_element_by_id('submit').click()
    time.sleep(3)

    while True:
        try:
            # input password
            WebDriverWait(browser, delay).until(expected_conditions.presence_of_element_located((By.ID,'j_password_user')))
            browser.find_element_by_id('j_password_user').send_keys(myPassword)
            WebDriverWait(browser, delay).until(expected_conditions.presence_of_element_located((By.ID,'submit')))
            browser.find_element_by_id('submit').click()
            print("Successfully logged in.\n")
            break

        except TimeoutException:
            continue

    # maximize browser window
    browser.maximize_window()

    # click 'Produk'
    WebDriverWait(browser, delay).until(expected_conditions.presence_of_element_located((By.LINK_TEXT,'Produk')))
    browser.find_element_by_link_text('Produk').click()

    # click 'Pelaburan Permulaan/Tambahan'
    WebDriverWait(browser, delay).until(expected_conditions.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[2]/div[1]/div[1]')))
    browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div[1]').click()

    # select fund for additional investment
    try:  
        WebDriverWait(browser, delay).until(expected_conditions.visibility_of_element_located((By.ID,selectedFund)))
        print('Operation Status:\tOPEN\n')
        print('Continue to select investment funds..\n')
        browser.find_element_by_id(selectedFund).click()
        print("Fund selected: " + asnbFund[myFund].get('fund_name') + "\n")
        
    except NoSuchElementException:
        print('Operation Status:\tCLOSED\n')
        print('Operating hours are 07:00 AM to 06:00 PM local time, Sunday to Friday and third Saturday of the month, excluding public holidays\n')
        print('Logging out...\n')
        browser.find_element_by_xpath("//*[contains(text(),'LOG KELUAR')]").click()
        print('Successfully logged out.\n')
        browser.close()
        sys.exit()

    # declaration of PEP
    WebDriverWait(browser, delay).until(lambda s: s.find_element_by_id("NEXT").is_displayed())
    browser.find_element_by_id('NEXT').click()

    # check the terms and condition checkbox (first attempt)
    browser.find_element_by_xpath('//*[@id="txnform"]/div/div[1]/div[4]/label/p').click

    # check if checkbox element is checked
    for i in range(10):
        try:
                browser.find_element_by_xpath('//*[@id="txnform"]/div/div[1]/div[4]/label/p').click()
                break

        except NoSuchElementException:
            print('Retry in 1s.')
            time.sleep(1)

        else:
            raise NoSuchElementException

    # click next button after checking the check box
    WebDriverWait(browser, delay).until(expected_conditions.presence_of_element_located((By.ID,'btn-unit-fund')))
    browser.find_element_by_id('btn-unit-fund').click()

    # input investment amount
    WebDriverWait(browser, delay).until(expected_conditions.visibility_of_element_located((By.NAME,'purchaseamount')))
    browser.find_element_by_name('purchaseamount').send_keys(myAmount)
    browser.find_element_by_id('btn-unit-fund').click()

    # starting to loop purchase attempt
    print("Starting purchase loop...\n")
    tesseract_lang = "six-percent-tesseract" # @ <C:\Program Files (x86)\Tesseract-OCR\tessdata\six-percent-tesseract.traineddata>
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
            right = location['x'] + 145 # size['width']
            bottom = location['y'] + size['height'] + 5

            im = Image.open(BytesIO(png))
            im = im.crop((left, top, right, bottom)) # defines crop points

            original_captcha = 'original_captcha'+'.png'

            # data collection
            # processed_captcha = '%s.png' %attempt # 'processed_captcha.png'

            # implementation mode
            processed_captcha = 'processed_captcha.png'
            
            save_captcha_image = im.save(original_captcha) #  saves new cropped image
            
            # read original asnb_captcha.png and pre-process it before applying Tesseract OCR
            img = cv2.imread(original_captcha,cv2.IMREAD_GRAYSCALE)

            # apply blur/resize/filter to captcha
            img = cv2.bilateralFilter(img,9,75,75)
            img = cv2.blur(img,(3,3))
            img = cv2.resize(img, (280,80))

            # binarize captcha
            (thres,img_bw) = cv2.threshold(img,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            cv2.imwrite(processed_captcha,img_bw)

            attempt = attempt + 1
            # apply OCR on the processed captcha image
            captcha_image = Image.open(processed_captcha)
            captcha_output = pytesseract.image_to_string(captcha_image, lang=tesseract_lang,config="-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 6")
            print("#" + str(attempt) + "\tCAPTCHA: "+ str(captcha_output))

            # enter captcha
            browser.find_element_by_xpath('//*[@id="defaultReal"]').send_keys(captcha_output)
            browser.find_element_by_id('btn-unit-fund').click()
            

            # captcha decode success rate data collection
            try:
                browser.find_element_by_xpath("//*[contains(text(),'Sila isi kod captcha yang sah')]")
                print('\tCaptcha Decode:\tFAILED\n')
                failure = failure + 1
                if attempt%10 == 0:
                    printSuccessRate(success, attempt)
                continue

            except NoSuchElementException:
                print('\tCaptcha Decode:\tSUCCESS\n')
                success = success + 1
                if attempt%10 == 0:
                    printSuccessRate(success, attempt)
                continue
                    
        # will enter exception when captcha element is no longer found
        except NoSuchElementException:
            print("Stopped purchasing loop, please take a look.\n")
            speak = win32com.client.Dispatch("SAPI.SpVoice")
            speak.Speak("Stopped purchasing loop, please take a look.")
            printDatalog(success, failure)
            printSuccessRate(success, attempt)

            print("Please remember to logout.\n")
            input("Press any key to exit program...\n")

            try:
                browser.close()
                sys.exit()

            except:
                print("Adios, " + myUser.title() + "! Have a great day!")
                sys.exit()
