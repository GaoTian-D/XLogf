#!/bin/bash

# Start the first process
flask --app flask_app run --host=0.0.0.0 --port=80 > /dev/null 2>&1 &
# Start the second process
python main.py &
# Wait for any process to exit
wait -n
# Exit with status of process that exited first
exit $?