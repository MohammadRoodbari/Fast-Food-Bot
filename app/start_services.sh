#!/bin/bash

# Start the Rasa actions server
cd chat_bot

rasa run actions &

# Start the Rasa server with specified options
rasa run -m models --enable-api --cors "*" --debug &

# Wait for a few seconds to ensure Rasa servers start
sleep 70

cd ..
# Start the main.py script
python main.py

# Prevent the script from exiting immediately
tail -f /dev/null
