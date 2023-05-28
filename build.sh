#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py migrate

echo "from scheduler.models import CustomUser; CustomUser.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
 
python manage.py collectstatic