#!/bin/sh

virtualenv () {
  echo "🔨 Activate virtual environment"
  . ./venv-six-percent/bin/activate
}


virtualenv 
while true
do
python main.py
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