#!/usr/bin/env bash
# -*- encoding: utf-8 -*-

# Deprecated use
# Bot now uses https://pypi.org/project/schedule/ to run its task every N minutes

red=$(tput setaf 1)

echo_error() {
  echo "$red✗ $1"
}

main() {
  while true; do
    pipenv run python3 main.py
    if [ "$?" -ne "0" ]; then echo_error "ERR - dependencies are not installed, please run ./setup.sh $1" && exit 1; fi
    echo "⏱  Retrying in 5 minutes..."
    sleep 60
    echo "⏱  Retrying in 4 minutes..."
    sleep 60
    echo "⏱  Retrying in 3 minutes..."
    sleep 60
    echo "⏱  Retrying in 2 minutes..."
    sleep 60
    echo "⏱  Retrying in 1 minutes..."
    sleep 60
  done
}

main
