# Six Percent
This is a bot which helps to automatically purchase ASNB Fixed Price UT units by solving the given CAPTCHA using Tesseract OCR. 

Currently this bot supports up to 3 fixed price unit trust at the moment:
- ASM (Malaysia)
- ASM2 (Wawasan)
- ASM3 (1Malaysia)

## Problem statement: Why do we need this bot?
- If there is no units available, you will never ever able to purchase new units or opening up a new account.
- You need to be able to solve the CAPTCHA automatically for every purchase attempt.

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the required modules for this project.

```bash
pip install -r requirements.txt
```

## Usage - How to run?
After you install the Tesseract-OCR using pip install above, put the tesseract.traineddata file inside your /tessdata folder in your installation path. (E.g.: C:\Program Files (x86)\Tesseract-OCR\tessdata\six-percent-tesseract.traineddata)


Inside the cloned project folder, run the six_percent.py from your Windows directly OR run the command line as below in your terminal:
```bash
python six_percent.py
```
Insert your username, password and the amount of units (in RM) that you would like to purchase, then click 'Start'
Proceed to make payment if you have successfully purchase any unit

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
N/A
