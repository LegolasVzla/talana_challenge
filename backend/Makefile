VENV_NAME?=env
HOST=127.0.0.1
DPORT=8001

help:
	@echo "make execute"
	@echo "	Run server."
	@echo "make setup"
	@echo "	Install packages and some default things needed in your system."
	@echo "make install"
	@echo "	By setting previously a virtual env, generate db with default data and install python requirements."

execute:
	python manage.py runserver ${HOST}:${DPORT}

celery:
	celery worker -A backend -f logs/--loglevel=INFO --autoscale=10,5 --concurrency=8

flower:
	flower --port=5555

setup:
	# Install PostgreSQL
	sudo apt-get update
	sudo apt install python3-dev postgresql postgresql-contrib python3-psycopg2 libpq-dev -y
	# Install RabbitMQ
	echo "deb http://www.rabbitmq.com/debian/ testing main"  | sudo tee  /etc/apt/sources.list.d/rabbitmq.list > /dev/null
	wget https://www.rabbitmq.com/rabbitmq-signing-key-public.asc
	sudo apt-key add rabbitmq-signing-key-public.asc
	sudo apt-get update
	sudo apt-get install rabbitmq-server -y
	sudo service rabbitmq-server start
	sudo rabbitmq-plugins enable rabbitmq_management
	sudo service rabbitmq-server restart
	# Generate log folder 
	mkdir logs
	# install pip
	sudo apt-get install python-pip python-dev build-essential -y
	sudo pip install --upgrade pip
	# install virtualenv
	sudo apt-get install python-virtualenv virtualenv -y
	pip install --upgrade virtualenv
	#apt --fix-broken install
	virtualenv $(VENV_NAME) --python=python3

install:
	pip install -r ../requirements.txt
	sudo -u postgres psql -c "CREATE DATABASE challenge_db WITH OWNER postgres;"
	python manage.py makemigrations
	python manage.py migrate
	# load default system data
	python manage.py insert_fixtures
