#!/bin/bash

# Restore the database from the most recent backup
if [ -f ./db/scripts/db_backup.sqlite3 ]; then
  echo "Restoring database from /db/scripts/db_backup.sqlite3"
  cp ./db/scripts/db_backup.sqlite3 /app/db.sqlite3
else
  echo "No backup file found."
fi
