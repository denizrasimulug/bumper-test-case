
dev:
	python manage.py runserver

migrations:
	python manage.py makemigrations
# python manage.py makemigrations <app_name> -n <migration_name>
# python manage.py makemigrations guestbook -n create_indices

migrate:
	python manage.py migrate

# admin:admin
superuser:
	python manage.py createsuperuser 

test:
	python manage.py test --tag=integration-test

loadtest:
	python manage.py test --tag=load-test

create_loadtest_data:
	python manage.py create_load_test_data
create_loadtest_db:
	python manage.py create_load_test_db