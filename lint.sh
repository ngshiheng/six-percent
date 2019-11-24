#!/usr/bin/env bash

# font color
red=$(tput setaf 1)
green=$(tput setaf 2)
white=$(tput sgr0)

PYVENV="venv-six-percent"

# function

activate_virtualenv() {
    echo "🔧 $white Activating virtual environment"
    source $PYVENV/bin/activate
    if [ "$?" -ne "0" ]; then echo_error "ERR - Virtual environment not found, please run ./setup.sh $1" && exit 1; fi
}

echo_finish() {
    echo "$green✓$white Finished checking"
}

echo_ok() {
    echo "$green✓$white $1"
}

echo_error() {
    echo "$red✗$white $1"
}

lint_check() {
    echo "⌛ $white Running flake8"
    flake8
    if [ "$?" -ne "0" ]; then echo_error "ERR - error while running flake8" && exit 1; fi
    echo "⌛ $white Running autopep8"
    autopep8 --in-place --aggressive -v main.py
    if [ "$?" -ne "0" ]; then echo_error "ERR - error while running autopep8" && exit 1; fi
    echo_ok "OK - no formatting or linting errors found"
}

main() {

    # if virtualenv is activated, then run lint check
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        echo "🔧 $white Virtual environment activated"
        lint_check
        echo_finish
    else
        activate_virtualenv
        lint_check
        echo_finish
    fi
}

main
