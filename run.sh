#!/bin/sh

# Check if migrations folder exists
if [ ! -d "./migrations" ];
then
    echo "Creating tables..."
    flask --app server db init
fi

# Check if there are any changes to the database
if flask --app server db check | grep "No changes detected";
then
    echo "No database changes detected"
else
    echo "Database changes detected! Migrating..."
    flask --app server db migrate
    flask --app server db upgrade
fi

# Start server!!!!
echo "Starting server..."
# gunicorn --bind highscore:8080 server:app