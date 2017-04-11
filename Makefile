clean:
	@find -type d -name migrations | xargs rm -rf
	@find -type d -name __pycache__ | xargs rm -rf

reset_db:
	@if [ -e "wallet/mydatabase" ]; then rm wallet/mydatabase; fi;

makemigrations:
	python bin/manage.py makemigrations accounts transactions

migrate:
	python bin/manage.py migrate

create_db:
	python bin/create_db.py

reset_migrate_createdb: clean reset_db makemigrations migrate create_db
