# classification_django
python -m venv .
chmod 755 ./bin/activate
. ./bin/activate
pip install -r requirements.txt

django-admin startapp csvapp
python manage.py makemigrations
ln csvapp/migration.py csvapp/migrations/migration.py

python manage.py migrate
python manage.py loaddata embedding_models
python manage.py loaddata category_hint 
python manage.py runserver

python manage.py showmigrations
python manage.py makemigrations --merge

redo migration pre requisite:
drop table django_admin_log ;
drop table auth_group_permissions;
drop table auth_user_user_permissions;
drop table auth_permission;
drop table django_content_type;
drop table auth_user_groups;
drop table auth_group;
drop table auth_user;
drop table django_session;
drop table class_embedding;
drop table ground_truth;
drop table public.ground_truth_classes;
drop table input_embedding;
drop table public.ground_truth_input;
drop table category_hint;
drop table public.embedding_models;

mv csvapp temp_csvapp
classification_django/settings.py - comment csvapp
django-admin startapp csvapp
classification_django/settings.py - uncomment csvapp
mv temp_csvapp/* csvapp/ 
mv  temp_csvapp/.venv csvapp/ 
mv  temp_csvapp/migrations/migration.py csvapp/migrations/migration.py
rm -rf temp_csvapp/migrations
rmdir temp_csvapp
