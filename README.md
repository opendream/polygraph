pip install -r requirements.txt
python manage.py syncdb
python manage.py migrate account
python manage.py migrate domain
python manage.py initial

# optional
python manage.py makesample
