# talana_challenge

## Technologies
- [Django](https://www.djangoproject.com/) the web framework for perfectionists with deadlines.

- [Django REST framework](https://www.django-rest-framework.org/) is a powerful and flexible toolkit for building Web APIs.

- [PostgreSQL](https://www.postgresql.org/) is the World's Most Advanced Open Source Relational Database.

- [Celery](https://pypi.org/project/django-celery/) Distributed Programming framework for Python.

- [Flower - Celery](https://flower.readthedocs.io/en/latest/) is a web based tool for monitoring and administrating Celery clusters

- [RabbitMQ](https://www.rabbitmq.com/) is the most widely deployed open source message broker.

## Installation

Clone this project:

	git clone https://github.com/LegolasVzla/talana_challenge

```Makefile``` will help you with all the installation. First of all, in ```talana_challenge/backend/``` path, execute:

	make setup

This will install PostgreSQL and pip on your system. After that, you need to create and fill up **settings.ini** file, with the structure as below:

	[postgresdbConf]
	DB_ENGINE=django.db.backends.postgresql
	DB_NAME=<dbname>
	DB_USER=<user>
	DB_PASS=<password>
	DB_HOST=<host>
	DB_PORT=<port>

	[timeZone]
	TIME_ZONE = UTC

	[emailConfig]
	EMAIL_HOST=<host>
	EMAIL_PORT=<port>
	EMAIL_HOST_USER=<origin_email> 
	EMAIL_HOST_PASSWORD=<origin_password_email>
	EMAIL_USER_TLS=True

	[rabbitMQConfig]
	RABBITMQ_USER=<rabbitmq_user>
	RABBITMQ_PASS=<rabbitmq_password>

	[frontendClient]
	FRONTEND_DOMAIN=<host>
	FRONTEND_PORT=<port>

- postgresdbConf section: fill in with your own PostgreSQL credentials. By default, DB_HOST and DB_PORT in PostgreSQL are localhost/5432 and db_challenge the database.

- frontendClient section: refers to the frontend port

- emailConfig section: if you use gmail domain, fill up ```EMAIL_HOST = smtp.gmail.com``` and ```EMAIL_PORT = 587```. Remember to activate [Unsafe application access](https://myaccount.google.com/lesssecureapps) of your email account.

- rabbitMQConfig section: by default ```RABBITMQ_USER``` and ```RABBITMQ_PASS``` are ```guest```

Then, activate your virtualenv already installed (by default, is called ```env``` in the ```Makefile```):

	source env/bin/activate

And execute:

	make install

This will generate the database with default data and also it will install python requirements and nltk resources. Default credentials for admin superuser are: admin@admin.com / admin. 

Run django server (by default, host and port are set as 127.0.0.1 and 8000 respectively in the ```Makefile```):

	make execute

You could see swagger doc in:

	http://127.0.0.1:8000/swagger/

In another terminal, run celery:

	make celery

Optionally you can run flower in another terminal too:

	make flower

You can monitoring rabbitMQ in:

	http://localhost:15672/#/

## Swagger Documentation

[Swagger UI](https://swagger.io/tools/swagger-ui/) is a tool for API documentation. "Swagger UI allows anyone — be it your development team or your end consumers — to visualize and interact with the API’s resources without having any of the implementation logic in place. It’s automatically generated from your OpenAPI (formerly known as Swagger) Specification, with the visual documentation making it easy for back end implementation and client side consumption."

This project uses [drf-yasg - Yet another Swagger generator](https://github.com/axnsan12/drf-yasg)

## Endpoints and Actions:

Endpoint Path |HTTP Method | CRUD Method | Used for
-- | -- |-- |--
`api/user/create_account/` | POST | Create user account. This endpoint will send you the email with the link to activate your account
`api/user/verify_account/<int:user_id>` | POST | Verify user account from email activation
`api/user/generate_password/(?P<pk>\d+)`| POST | Generate password to an user account
`api/user/choose_winner/` | POST | Generate a winner

