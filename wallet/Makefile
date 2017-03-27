clean:
	@find -type d -name migrations | xargs rm -rf
	@find -type d -name __pycache__ | xargs rm -rf

reset_db:
	@sudo su postgres -c 'dropdb thetldb'
	@sudo su postgres -c 'psql -c "CREATE DATABASE thetldb"'
	@sudo su postgres -c 'psql -c "GRANT ALL PRIVILEGES ON DATABASE thetldb TO jshcrm"'

makemigrations:
	python manage.py makemigrations accounts transactions

migrate:
	python manage.py migrate

create_db:
	python create_db.py

reset_migrate_createdb: clean reset_db makemigrations migrate create_db
