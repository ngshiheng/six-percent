#!/usr/bin/env bash

################################################################################
################################################################################
################################################################################
#                                                                              #
#   DEPRECATED                                                                 #
#                                                                              #
################################################################################
################################################################################
################################################################################

echo -e "LOG_WARN     Deprecated !!!!!"
echo -e "$LOG_WARN =================================================================="

red=$(tput setaf 1)
green=$(tput setaf 2)
white=$(tput sgr0)

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
    pipenv run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    pipenv run flake8 . --count --exit-zero --max-complexity=20 --max-line-length=255 --statistics
    if [ "$?" -ne "0" ]; then echo_error "ERR - error while running flake8" && exit 1; fi
    echo "⌛ $white Running autopep8"
    pipenv run autopep8 --in-place --aggressive -v main.py
    if [ "$?" -ne "0" ]; then echo_error "ERR - error while running autopep8" && exit 1; fi
    echo_ok "OK - no formatting or linting errors found"
}

main() {
    lint_check
    if [ "$?" -ne "0" ]; then echo_error "ERR - dependencies are not installed, please run ./setup.sh $1" && exit 1; fi
    echo_finish
}

main
