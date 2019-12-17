# Six Percent :money_with_wings:

This bot helps user to automatically purchase ASNB Fixed Price UT units. The bot will trigger the user to proceed to make payment if the purchase attempt is successful.

Currently this bot supports up to 3 fixed price unit trust:

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

### Software :computer:

- Python 3.6+
- [pip](https://pip.pypa.io/en/stable/) package installer
- Python [virtual environment](https://virtualenv.pypa.io/en/latest/)
- [chromedriver](https://chromedriver.chromium.org/downloads) based off your OS & Chrome version

**File configuration:**
- Rename `users.json.example` to `users.json` and update the information accordingly
- Configure `funds.json` accordingly, if the specific fund you own is categorized under initial investment or additional investment
  - E.g.: If the specific fund you have on your account is an initial investment, set `"initial_investment": true`
  

#### Installation (Ubuntu) :wrench:

```bash
apt-get update && apt-get install -y --no-install-recommends python3 python3-virtualenv python3-pip chromium-chromedriver locales

locale-gen en_US.UTF-8
```

### Opening ASNB Account :closed_lock_with_key:

- You need a ASNB account in order to start investing
- You can perform all the transactions (including opening an account) at any ASNB branches or agents

## Setup & Run :nut_and_bolt:

This project is tested and developed on Ubuntu 18.04 LTS.

Run `./setup.sh` to install all the Python dependencies

Run `./run.sh` to start using the bot

## Contributing :family:

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please run `./lint.sh` before commiting any code and make sure it passes all the lint and format check

### Steps 
1. Fork this
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## License :copyright:

six-percent is released under the MIT license.

Copyright (c) 2019 Jerry Ng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
