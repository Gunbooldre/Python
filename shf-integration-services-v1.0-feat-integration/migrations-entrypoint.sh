#!/bin/bash
set -o errexit  
set -o pipefail  

python manage.py makemigrations  
python manage.py migrate

exec "$@"