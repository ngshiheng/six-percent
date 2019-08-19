# Six Percent
This is a bot which helps to automatically purchase ASNB Fixed Price UT units by solving the given CAPTCHA using Tesseract OCR. 

This project is developed and tested on Windows.

Currently this bot supports up to 3 fixed price unit trust:
- ASM (Malaysia)
- ASM2 (Wawasan)
- ASM3 (1Malaysia)

## About myASNB Fixed Price Mutual Fund
![alt text](https://i.imgur.com/LCB8Soo.jpg)
- If there is no units available, you will never ever able to purchase new units or opening up a new account.
- You need to be able to solve the CAPTCHA automatically for every purchase attempt.
- For more details, visit the [myASNB Official Website](https://www.myasnb.com.my/)

## Installation & Setup
Create a virtual environment using Python **venv**
```
python -m venv venv-six-percent
```


Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the required modules for this project.
```
pip install -r requirements.txt
```

After installing all the requirements, place `six-percent-tesseract.traineddata` inside the installation path `Tesseract-OCR/tessdata` (E.g.: `C:\Program Files (x86)\Tesseract-OCR\tessdata\six-percent-tesseract.traineddata`).

Add your Tesseract-OCR installation path (E.g. `C:\Program Files (x86)\Tesseract-OCR\tessdata`) to your **Path** & **TESSDATA_PREFIX** environment variable. 

*Note: create a new environment variable called TESSDATA_PREFIX if it doesn't exist*

## Usage

Inside the cloned project folder, execute the `six_percent.py` from your Windows directly OR run the command line as below in your terminal:
```bash
python six_percent.py
```
Enter your username, password, fund choice and the amount of units (in RM) that you would like to purchase, then the bot will automatically do what it does best. :)

Proceed to make payment if purchase attempt is successful.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)