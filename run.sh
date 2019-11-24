#!/usr/bin/env bash
# -*- encoding: utf-8 -*-

red=$(tput setaf 1)
PYVENV="venv-six-percent"

activate_virtualenv() {

  echo "🔨 Activate virtual environment"
  . ./$PYVENV/bin/activate
  if [ "$?" -ne "0" ]; then echo_error "ERR - Virtual environment not found, please run ./setup.sh $1" && exit 1; fi

}

echo_error() {
  echo "$red✗ $1"
}

main() {
  activate_virtualenv
  while true; do
    python3 main.py
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
