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

green=$(tput setaf 2)
white=$(tput sgr0)

setup_virtualenv() {
    echo "🛠 $white Removing existing virtualenv"
    pipenv --rm
    echo "🔧 $white Activating virtual environment"
    pipenv shell
}

pipenv_install() {
    echo "🐍 $white Installing Python dependencies with pipenv"
    pipenv install --dev
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
