
dev:
	python manage.py runserver --settings=bumperguest.settings.dev

migrations:
	python manage.py makemigrations --settings=bumperguest.settings.dev
# python manage.py makemigrations <app_name> -n <migration_name>
# python manage.py makemigrations guestbook -n create_indices

migrate:
	python manage.py migrate --settings=bumperguest.settings.dev

# admin:admin
superuser:
	python manage.py createsuperuser  --settings=bumperguest.settings.dev

test:
	python manage.py test --tag=integration-test --settings=bumperguest.settings.dev

loadtest:
	python manage.py test --tag=load-test --settings=bumperguest.settings.loadtest

create_loadtest_data:
	python manage.py create_load_test_data


deps:
	pip install -r requirements.txt

run_postgre:
	docker stop postgres-instance-bumper
	docker rm postgres-instance-bumper
	docker run --name postgres-instance-bumper \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=load_test_database \
  -p 5432:5432 \
  -d postgres
