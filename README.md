# Six Percent :money_with_wings:

This bot helps user to automatically purchase ASNB Fixed Price UT units. User shall proceed to make their own payment if there is a successful purchase attempt.

Currently, this bot supports up to 3 fixed price unit trust:

- ASM (Malaysia)
- ASM2 (Wawasan)
- ASM3 (1Malaysia)

_Note: As of Q3 2019, ASNB removed the need of solving CAPTCHA in order to purchase any ASNB Fixed Price UT_

## About myASNB Fixed Price Fund :moneybag:

ASNB is a subsidiary of “Permodalan Nasional Berhad” (PNB). It is a government-supported unit trust management company.

Amanah Saham are funds that are managed by Amanah Saham National Berhad (ASNB)

![alt text](https://i.imgur.com/LCB8Soo.jpg)

### Facts :newspaper:

- If there is no units available, you will never be able to purchase new units or opening up a new account
- Fixed price (RM 1/unit) means there will be no price fluctuation. These funds can thus be regarded as saving accounts
- The dividend earned is not taxable
- No sales charge

For more details, visit the [myASNB Official Website](https://www.myasnb.com.my/)

## Requirements & Dependencies

### Opening ASNB Account :closed_lock_with_key:

- You need a ASNB account in order to start investing
- You can perform all the transactions (including opening an account) at any ASNB branches or agents

### Software :computer:

- Python 3.6+
- [pip](https://pip.pypa.io/en/stable/) package installer
- Python [virtual environment](https://virtualenv.pypa.io/en/latest/)
- [chromedriver](https://chromedriver.chromium.org/downloads) based off your OS & Chrome version

### File configuration :document:

- Rename `users.json.example` to `users.json` and add/update the information accordingly. Change `"is_active": false` if you do not want to use the user
- Configure `funds.json`, set `"skip": true` if you do **NOT** want to buy that specific fund

#### Installation (Ubuntu) :wrench:

```bash
apt-get update && apt-get install -y --no-install-recommends python3 python3-virtualenv python3-pip chromium-chromedriver locales

locale-gen en_US.UTF-8
```

## Setup & Run :nut_and_bolt:

This project is tested and developed on Ubuntu 18.04 LTS. You can probably get this up and running on Windows or Mac with some minor tweaks.

Run `./setup.sh` to install all the Python dependencies

Run `./run.sh` to start using the bot with scheduler (5 minutes)

To run only once, run `python3 main.py`

## Contributing :family:

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Steps

1. Fork this
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Please run `./lint.sh` before commiting any code and make sure it passes all the lint and format check
4. Commit your changes (`git commit -am 'Add some fooBar'`)
5. Push to the branch (`git push origin feature/fooBar`)
6. Create a new Pull Request
