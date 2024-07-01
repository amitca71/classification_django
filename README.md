# classification_django
python -m venv .
chmod 755 ./bin/activate
. ./bin/activate
pip install -r requirements.txt

django-admin startapp csvapp
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata embedding_models
python manage.py loaddata category_hint 
python manage.py runserver

python manage.py showmigrations
python manage.py makemigrations --merge

