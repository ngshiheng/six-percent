#!/usr/bin/env bash

# font color
green=$(tput setaf 2)
white=$(tput sgr0)

# functions
setup_virtualenv() {
    echo "🛠 $white Removing existing virtualenv"
    pipenv --rm
    echo "🔧 $white Activating virtual environment"
    pipenv shell
}

pipenv_install() {
    echo "🐍 $white Installing Python dependencies with pipenv"
    pipenv install
    echo "$green✔$white Completed pipenv install"
}

echo_finish() {
    echo "$green✔$white$1 Finished setup"
}

main() {
    setup_virtualenv
    pipenv_install
    echo_finish
}

main
