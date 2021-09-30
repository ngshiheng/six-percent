<h1 align="center">Six Percent</h1>

![Build executables](https://github.com/ngshiheng/six-percent/workflows/Build%20executables/badge.svg?branch=master)
![Lint check](https://github.com/ngshiheng/six-percent/workflows/Lint%20check/badge.svg?branch=master)

Please read the [disclaimer](#Disclaimer) section before using.

This bot helps user to automatically purchase [ASNB Fixed Price UT units](#FAQ).

User shall proceed to **make their own payment** if there is a successful purchase attempt.

Currently, this bot supports up to 3 fixed price unit trust:

-   ASM (Malaysia)
-   ASM2 (Wawasan)
-   ASM3 (1Malaysia)

---

## Development Requirements

-   Python 3.8+
-   [pip](https://pip.pypa.io/en/stable/) package installer
-   [pipenv](https://pypi.org/project/pipenv/)
-   [chromedriver](https://chromedriver.chromium.org/downloads) based on your OS & [Chrome version](chrome://settings/help)

### Installation (Windows 10/11)

Run `pip install pipenv` See [this](https://stackoverflow.com/questions/46041719/windows-reports-error-when-trying-to-install-package-using-pipenv) post if you encounter any error with `pipenv`

Start by installing all the dependencies

```bash
# At project directory
pipenv shell
pipenv install --dev
```

**Option 1: Run this project directly with python:**

```bash
python main.py
```

**Option 2: Run this project with `exe` file:**

1. To generate a `exe` application, run

```sh
pyi-makespec main.py --name SixPercent --icon "bin\favicon.ico" --onefile --console --add-binary "bin\driver\chromedriver.exe;bin\driver\\"
```

2. Finally run `pyinstaller SixPercent.spec --clean`

3. Run the `SixPercent.exe` directly inside generated the `dist` folder

## How to use with python:

1. Run `pipenv run python main.py`

2. Proceed to make your own payment if purchasing attempt is successful. Always remember to logout and restart the bot manually (exit and run again).

3. If purchase attempt is unsuccessfully this time, the bot will repeat the attempt every 5 minutes.

## How to use with executable (Windows only):

Refer to Installation (Windows) option 2 if the `SixPercent.exe` is not generated yet

1. Run `SixPercent.exe` directly -> click 'Login as new user' -> Fill in your credentials -> click 'Start'

2. Proceed to make your own payment if purchasing attempt is successful. Always remember to logout and restart the bot manually (exit and run again).

3. Kill the program and re-run it after payment is made

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Steps

1. Fork this
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Please run `./scripts/lint.sh` before commiting any code and make sure it passes all the lint and format check
4. Commit your changes (`git commit -am 'Add some fooBar'`)
5. Push to the branch (`git push origin feature/fooBar`)
6. Create a new Pull Request

---

## Disclaimer

> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

-   This software comes with no warranties of any kind whatsoever, and may not be useful for anything. Use it at your own risk!
-   This software was designed to be used only for research purposes.
-   Uses are not recommended, and have never been evaluated.
-   If these terms are not acceptable, you aren't allowed to use the code.

---

## FAQ

> What is myASNB Fixed Price Fund?

-   ASNB is a subsidiary of “Permodalan Nasional Berhad” (PNB). It is a government-supported unit trust management company.
-   Amanah Saham are funds that are managed by Amanah Saham National Berhad (ASNB)

> How does the fund work? Why do I care?

-   If there is no units available, you will never be able to purchase new units or opening up a new account
-   Fixed price (RM 1/unit) means there will be no price fluctuation. These funds can thus be regarded as saving accounts

> Tax?

-   The dividend earned is not taxable

> Fees?

-   No sales charge

> How to start buying?

-   You need a ASNB account in order to start investing
-   You can perform all the transactions (including opening an account) at any ASNB branches or agents

For more details, visit [myASNB Official Website](https://www.myasnb.com.my/)
