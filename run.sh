#!/usr/bin/env bash
# -*- encoding: utf-8 -*- 

virtualenv () {
  echo "🔨 Activate virtual environment"
  . ./venv-six-percent/bin/activate
}

virtualenv 

while true
  do
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