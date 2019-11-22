#!/usr/bin/env bash

#################################################################################
# 
#   Create a virtualenv before running this setup.sh script
#   
#       python3 -m venv virtual-env-name
#   
#################################################################################

# font color
red=`tput setaf 1`
green=`tput setaf 2`
white=`tput sgr0`

# functions
setup_virtualenv () {
    python3 -m virtualenv venv-six-percent --no-site-packages
}

pip_install () {
    pip3 install -r requirements.txt
    echo "🐍 $white Installing dependencies with pip"
    echo "$green✔$white Completed pip install"
}

echo_finish () {
    echo "$green✔$white Finished setup."
}

# main
setup_virtualenv
pip_install
echo_finish