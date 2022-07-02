<h1 align="center">Six Percent</h1>

<p align="center">
  <img src="https://imgur.com/IYGMoUo.png">
</p>
<br />

[![build](https://github.com/ngshiheng/six-percent/actions/workflows/build.yml/badge.svg)](https://github.com/ngshiheng/six-percent/actions/workflows/build.yml)
[![lint](https://github.com/ngshiheng/six-percent/actions/workflows/lint.yml/badge.svg)](https://github.com/ngshiheng/six-percent/actions/workflows/lint.yml)
[![release](https://github.com/ngshiheng/six-percent/actions/workflows/release.yml/badge.svg)](https://github.com/ngshiheng/six-percent/actions/workflows/release.yml)

Please read the [disclaimer](./docs/DISCLAIMER.md) before using.

This bot helps users to buy [ASNB Fixed Price UT units](#FAQ).

The user shall proceed to **make his/her own payment** ([M2U](https://www.maybank2u.com.my/) only) if there is a successful purchase attempt.

Currently, this bot supports up to 3 fixed price unit trusts:

-   ASM (Malaysia)
-   ASM2 (Wawasan)
-   ASM3 (1Malaysia)

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Development](#development)
  - [Requirements](#requirements)
  - [Installation (Windows 10/11)](#installation-windows-1011)
  - [Run with Python](#run-with-python)
  - [Compiling to `exe`](#compiling-to-exe)
- [Usage](#usage)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)
- [FAQ](#faq)

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

## Usage

Read [USAGE.md](./docs/USAGE.md).

## Contributing

Read [CONTRIBUTING.md](./docs/CONTRIBUTING.md).

## Disclaimer

Read [DISCLAIMER.md](./docs/DISCLAIMER.md).

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
