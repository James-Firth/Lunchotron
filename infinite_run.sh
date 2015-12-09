#!/bin/bash

while true; do
	python runbot.py
	echo "Uh oh the bot died. Starting up a  new one in 5s..."
	sleep 5s;
done;
