# Six Percent

![Build executables](https://github.com/ngshiheng/six-percent/workflows/Build%20executables/badge.svg?branch=master)
![Lint check](https://github.com/ngshiheng/six-percent/workflows/Lint%20check/badge.svg?branch=master)

> _DISCLAIMER: Please use this at your own risk_

This bot helps user to automatically purchase ASNB Fixed Price UT units.

User shall proceed to make their own payment if there is a successful purchase attempt.

Currently, this bot supports up to 3 fixed price unit trust:

- ASM (Malaysia)
- ASM2 (Wawasan)
- ASM3 (1Malaysia)

## About myASNB Fixed Price Fund

ASNB is a subsidiary of “Permodalan Nasional Berhad” (PNB). It is a government-supported unit trust management company.

Amanah Saham are funds that are managed by Amanah Saham National Berhad (ASNB)

![alt text](https://i.imgur.com/LCB8Soo.jpg)

### Facts

- If there is no units available, you will never be able to purchase new units or opening up a new account
- Fixed price (RM 1/unit) means there will be no price fluctuation. These funds can thus be regarded as saving accounts
- The dividend earned is not taxable
- No sales charge

For more details, visit [myASNB Official Website](https://www.myasnb.com.my/)

## Requirements & Dependencies

### Opening ASNB Account

- You need a ASNB account in order to start investing
- You can perform all the transactions (including opening an account) at any ASNB branches or agents

### Software

- Python 3.8
- [pip](https://pip.pypa.io/en/stable/) package installer
- [pipenv](https://pypi.org/project/pipenv/)
- [chromedriver](https://chromedriver.chromium.org/downloads) based on your OS & Chrome version

### User Configuration

Update `config.ini` to edit your `chromedriver` path. **Please note that your `chromedriver` path might be different from the default settings in `config.ini`**

### Installation (Ubuntu)

This project is tested and developed on `Ubuntu 20.04.01 LTS`. You can probably get this up and running on Mac with some minor tweaks

For Ubuntu user please remember to update your `chromedriver` path at `config.ini`

```bash
apt-get update && apt-get install -y --no-install-recommends python3 python3-virtualenv python3-pip chromium-chromedriver locales

locale-gen en_US.UTF-8

# At project directory
pipenv shell
pipenv install --dev

python3 main.py
```

Run `./scripts/setup.sh` to install all the Python dependencies

### Installation (Windows)

This project is also tested on `Windows 10`

Run `pip install pipenv` See [this](https://stackoverflow.com/questions/46041719/windows-reports-error-when-trying-to-install-package-using-pipenv) post if you encounter any error with pipenv

**Option 1: Run this project directly with python:**

```bash
# At project directory
pipenv shell
pipenv install --dev

python main.py
```

**Option 2: Run this project with `exe` file:**
To generate a `exe` application, run

```sh
pipenv shell
pipenv install --dev

pyi-makespec main.py --onefile --add-binary "bin\driver\chromedriver.exe;bin\driver\" --add-data "config.ini;." --name SixPercent --icon "bin\favicon.ico"  --console
```

Then append the code block below at the **end** of the generated `SixPercent.spec`. See [example](SixPercent.spec)

```spec
import shutil
shutil.copyfile('config.ini', '{0}/config.ini'.format(DISTPATH))
```

Finally run `pyinstaller SixPercent.spec`

Run the `SixPercent.exe` directly inside generated the `dist` folder! :)

## How to use with python:

1. Run `pipenv run python3 main.py`

2. Job to purchase ASNB unit will start based on your configuration at `config.ini`. Please note that if the bot doesn't work. Try to increase `min_seconds`

3. Proceed to make your own payment if purchasing attempt is successful. Always remember to logout and restart the bot manually (exit and run again).

4. If purchase attempt is unsuccessfully this time, the bot will repeat the attempt every 5 minutes (Able to modify in `config.ini` under `minutes`)

## How to use with executable (Windows only):

Refer to Installation (Windows) option 2 if the `SixPercent.exe` is not generated yet

1. Run `SixPercent.exe` directly

2. Proceed to make your own payment if purchasing attempt is successful. Always remember to logout and restart the bot manually (exit and run again).

3. Kill the program and re-run it after payment is made

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Steps

1. Fork this
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Please run `./scripts/lint.sh` before commiting any code and make sure it passes all the lint and format check
4. Commit your changes (`git commit -am 'Add some fooBar'`)
5. Push to the branch (`git push origin feature/fooBar`)
6. Create a new Pull Request

## Disclaimer

> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

This software was designed to be used only for research purposes.

Uses are not recommended, and have never been evaluated.

This software comes with no warranties of any kind whatsoever, and may not be useful for anything. Use it at your own risk!

If these terms are not acceptable, you aren't allowed to use the code.
