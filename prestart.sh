#! /usr/bin/env sh
# shellchecl shell=dash

if [ -z "$DB_CONNECTION" ]; then
  echo "DB_CONNECTION environment variable not set!!!" >&2
  exit 1
fi

# Let the DB start
python ./app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python ./app/initial_data.py
