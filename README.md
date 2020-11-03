# talana_challenge


## Installation

Clone this project:

	git clone https://github.com/LegolasVzla/talana_challenge

```Makefile``` will help you with all the installation. First of all, in ```talana_challenge/backend/``` path, execute:

	make setup

This will install PostgreSQL and pip on your system. After that, you need to create and fill up **settings.ini** file, with the structure as below:

	[postgresdbConf]
	DB_ENGINE=django.db.backends.postgresql
	DB_NAME=dbname
	DB_USER=user
	DB_PASS=password
	DB_HOST=host
	DB_PORT=port

	[frontendClient]
	FRONTEND_DOMAIN=<host>
	FRONTEND_PORT=<port>

- postgresdbConf section: fill in with your own PostgreSQL credentials. By default, DB_HOST and DB_PORT in PostgreSQL are localhost/5432.

- frontendClient section: refers to the fronend port

Then, activate your virtualenv already installed (by default, is called ```env``` in the ```Makefile```):

	source env/bin/activate

And execute:

	make install

This will generate the database with default data and also it will install python requirements and nltk resources. Default credentials for admin superuser are: admin@admin.com / admin. 

Run django server (by default, host and port are set as 127.0.0.1 and 8000 respectively in the ```Makefile```):

	make execute

You could see swagger doc in:

	http://127.0.0.1:8000/swagger/
