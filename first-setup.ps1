pip install -r requirements.txt

python manage.py db init
python manage.py db migrate
python manage.py db upgrade

$host.enternestedprompt()