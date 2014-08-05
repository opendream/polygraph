# Install mysql and create database
# username password dbname config in polygraph/settings.py or create polygraph/settings_local.py override
mysql -u root -e "CREATE DATABASE polygraph DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci";

pip install -r requirements.txt
python manage.py syncdb
python manage.py migrate account
python manage.py migrate domain
python manage.py initial

# optional
python manage.py makesample
