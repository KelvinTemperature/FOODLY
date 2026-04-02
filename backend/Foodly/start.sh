#!/usr/bin/env bash
set -euo pipefail

python /app/wait_for_datastores.py
exec gunicorn -b 0.0.0.0:5000 app:app
