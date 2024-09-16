#!/bin/bash

# Define the backup file name with a timestamp
BACKUP_FILE="db/scripts/db_backup_$(date +%Y%m%d%H%M%S).sqlite3"

# Copy the SQLite database to the backup directory
cp /app/db.sqlite3 $BACKUP_FILE

echo "Database backup completed: $BACKUP_FILE"
