## Usage

-   Run `SixPercent.exe`
-   Click 'Login as new user' -> Fill in user info -> click 'Start'
-   If purchasing attempt is successful
    -   Proceed to make payment
    -   Kill the program and re-run it after payment is made
-   Otherwise, the bot will rerun every 5 minutes

Generally, there are 3 different ways you can run this bot:

### 1. Download and run executable (Windows):

> Easiest. For end user

1. Download from https://tinyurl.com/asnbsixpercent
2. Run

### 2. Compile and run executable (Windows):

> For development

1. Generate `SixPercent.exe` by following the steps [above](#compiling-to-exe)
2. Run

### 3. Run directly with Python

> For development

1. Run `poetry install --no-root`
2. Run `poetry run python main.py`
