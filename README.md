<h1 align="center">Six Percent</h1>

<p align="center">
  <img src="https://i.imgur.com/Z0cCIy9.png">
</p>
<br />

[![build](https://github.com/ngshiheng/six-percent/actions/workflows/build.yml/badge.svg)](https://github.com/ngshiheng/six-percent/actions/workflows/build.yml)
[![lint](https://github.com/ngshiheng/six-percent/actions/workflows/lint.yml/badge.svg)](https://github.com/ngshiheng/six-percent/actions/workflows/lint.yml)
[![release](https://github.com/ngshiheng/six-percent/actions/workflows/release.yml/badge.svg)](https://github.com/ngshiheng/six-percent/actions/workflows/release.yml)

Please read the [disclaimer](#Disclaimer) section before using.

This bot helps users to buy [ASNB Fixed Price UT units](#FAQ).

The user shall proceed to **make his/her own payment** ([M2U](https://www.maybank2u.com.my/) only) if there is a successful purchase attempt.

Currently, this bot supports up to 3 fixed price unit trusts:

-   ASM (Malaysia)
-   ASM2 (Wawasan)
-   ASM3 (1Malaysia)

---

## Development

### Requirements

-   Windows 10+
-   [python](https://www.python.org/) 3.8+
-   [pip](https://pip.pypa.io/en/stable/) package installer
-   [poetry](https://python-poetry.org/docs/)
-   [chromedriver](https://chromedriver.chromium.org/downloads) based on your OS & [Chrome version](chrome://settings/help)

### Installation (Windows 10/11)

We use [poetry](https://python-poetry.org/docs/basic-usage/) to manage our dependencies.

Start by installing all the dependencies

```sh
poetry install --no-root
pre-commit install
```

### Run with Python

```sh
poetry run python main.py
```

### Compiling to `exe`

Optional: to generate a new `SixPercent.spec` file, run the following:

```sh
pyi-makespec main.py --name SixPercent --icon "img\favicon.ico" --onefile --console --add-binary "bin\driver\chromedriver.exe;bin\driver\"
```

1. To (re)generate the executable, run `pyinstaller SixPercent.spec --clean`

2. A `SixPercent.exe` will be generated inside the `dist/` folder

3. Run `SixPercent.exe` and use the bot

---

## Usage

### Run with Python installed

1. Run `poetry run python main.py`

2. Proceed to make the payment if purchasing attempt is successful. Always remember to log out and restart the bot manually (exit and run again).

3. If the purchase attempt is unsuccessful this time, the bot will repeat the attempt every ~5 minutes.

### Run with executable (Windows only):

Generate `SixPercent.exe` by following the steps [above](#run-this-project-with-exe-file)

1. Run `SixPercent.exe` directly -> click 'Login as new user' -> Fill in your credentials -> click 'Start'

2. Proceed to make your own payment (currently only supports Maybank) if purchasing attempt is successful. Always remember to log out and restart the bot manually (exit and run again).

3. Kill the program and re-run it after payment is made

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Steps

1. Fork this
2. Create your feature branch (`git checkout -b add-foo-bar`)
3. Please make sure you have installed the `pre-commit` hook and make sure it passes all the checks
4. Commit your changes (`git commit -am 'feat: add some fooBar`', make sure that your [commits are semantic](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716))
5. Push to the branch (`git push origin add-foo-bar`)
6. Create a new Pull Request

---

## Disclaimer

> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

-   This software comes with no warranties of any kind whatsoever, and may not be useful for anything. Use it at your own risk!
-   This software was designed to be used only for research purposes.
-   Uses are not recommended and have never been evaluated.
-   If these terms are not acceptable, you aren't allowed to use the code.

---

## FAQ

For more details, visit [myASNB Official Website](https://www.myasnb.com.my/)

> What is myASNB Fixed Price Fund?

-   ASNB is a subsidiary of “Permodalan Nasional Berhad” (PNB). It is a government-supported unit trust management company.
-   Amanah Saham are funds that are managed by Amanah Saham National Berhad (ASNB).

> How does the fund work? Why should I care?

-   If there is no unit available, you will never be able to purchase new units or open up a new account.
-   A fixed price (RM 1/unit) means there will be no price fluctuation. These funds can thus be regarded as saving accounts.
-   The dividend earned is not taxable.

> Is there any sales charge or additional fees?

-   No sales charge.
-   No additional fees.

> How to start buying or investing?

-   You need an ASNB account in order to start investing.
-   You can perform all the transactions (including opening an account) at any ASNB branch or agent.
