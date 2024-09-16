#!/bin/bash

# Define the location of your database and backup folder
DB_FILE="../db.sqlite3"
BACKUP_DIR="backup"
BACKUP_FILE="$BACKUP_DIR/backup.sqlite3"

# Create the backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Check if the database file exists
if [ -f "$DB_FILE" ]; then
    # Backup the SQLite database
    cp $DB_FILE $BACKUP_FILE
    echo "Database backup created at $BACKUP_FILE"
else
    echo "Database file $DB_FILE not found!"
    exit 1
fi
