title Giveaway Hunter
@echo off

cls
:: For setting up
echo installing python dependencies....
pip install tweepy

cls
:: Setting up API keys
echo opening the key file in python IDLE
python -m idlelib example_hidden.py
echo After successfully setting up your keys
pause
ren example_hidden.py hidden.py

cls
echo add some of your twitter friends username separated by a new line
echo Ex: @rahulsharma9000
notepad frens.txt
pause

cls
echo python fetch.py > StartHere.bat
echo This script will now self-destruct.
echo Start the Script from "StartHere.bat"
pause
(goto) 2>nul & del "%~f0"
