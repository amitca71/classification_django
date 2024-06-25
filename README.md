# classification_django
python -m venv .
./bin/activate
pip install -r requirements.txt

django-admin startapp csvapp
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

