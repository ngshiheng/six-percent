# Six Percent :money_with_wings:

This bot helps user to automatically purchase ASNB Fixed Price UT units. User shall proceed to make their own payment if there is a successful purchase attempt.

Currently, this bot supports up to 3 fixed price unit trust:

- ASM (Malaysia)
- ASM2 (Wawasan)
- ASM3 (1Malaysia)

Please **use this software at your own risk**!
Please read the disclaimer section.

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

Please read carefully.

### Opening ASNB Account :closed_lock_with_key:

- You need a ASNB account in order to start investing
- You can perform all the transactions (including opening an account) at any ASNB branches or agents

### Software :computer:

- Python 3.6+
- [pip](https://pip.pypa.io/en/stable/) package installer
- [pipenv](https://pypi.org/project/pipenv/)
- [chromedriver](https://chromedriver.chromium.org/downloads) based off your OS & Chrome version (Important!!!)

### File configuration :document:

- Rename `users.json.example` to `users.json` and add/update the information accordingly. Change `"is_active": false` if you do not want to use the user
- Configure `funds.json`, set `"skip": true` if you do **NOT** want to buy that specific fund

#### Installation (Ubuntu) :wrench:

This project is tested and developed on Ubuntu 18.04 LTS. You can probably get this up and running on Windows or Mac with some minor tweaks.

```bash
apt-get update && apt-get install -y --no-install-recommends python3 python3-virtualenv python3-pip chromium-chromedriver locales

locale-gen en_US.UTF-8
```

Run `./setup.sh` to install all the Python dependencies

Run `./run.sh` to start using the bot with scheduler (5 minutes)

#### Installation (Windows)

_Coming soon..._

#### Installation (MacOS)

_Coming soon..._

## Setup & Run :nut_and_bolt:

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

## Disclaimer

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

This software was designed to be used only for research purposes.
Uses are not recommended, and have never been evaluated.
This software comes with no warranties of any kind whatsoever,
and may not be useful for anything. Use it at your own risk!
If these terms are not acceptable, you aren't allowed to use the code.
