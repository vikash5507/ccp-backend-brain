# README #

Setup steps:

1. Make sure you have python 3 and pip installed. With pip you can install Django. "pip install Django".
2. Install dependencies:
	- pip install django-phonenumber-field
	- Install dependency for geodjango (platform dependent)
3. Clone this repository.
4. In the ccp_backend folder (this is the folder containing manage.py file), open a terminal.
5. Make migrations and migrate, this will setup the database!
	- python manage.py makemigrations
	- python manage.py migrate
6. Create a superuser. This will grant you access to the admin site.
	- python manage.py createsuperuser
	Follow the instructions in the interactive command line.
7. Run the server.
	- python manage.py runserver
	This will print a localhost url where the django server is up and running. go to http://127.0.0.1:8000/admin to access the admin site. Login using the credentials you set in the creating superuser phase.
	