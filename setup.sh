#!/usr/bin/env bash

# font color
green=`tput setaf 2`
white=`tput sgr0`

# functions
setup_virtualenv () {
    echo "🛠 $white Removing existing venv-six-percent"
    rm -rf venv-six-percent
    virtualenv venv-six-percent
    echo "🔧 $white Activating virtual environment"
    source venv-six-percent/bin/activate
}

pip_install () {
    echo "🐍 $white Installing Python dependencies with pip"
    pip3 install -r requirements.txt
    echo "$green✔$white Completed pip install"
}

echo_finish () {
    echo "$green✔$white$1 Finished setup"
}

# main
setup_virtualenv
pip_install
echo_finish 