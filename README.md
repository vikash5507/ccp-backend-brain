# README #

### Local Machine Setup steps: ###

1. Make sure you have python 3 and pip installed. With pip you can install Django. "pip install Django".
2. Install dependencies:
	- pip install django-phonenumber-field
	- pip install phonenumbers
	- pip install djangorestframework
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


### Docker Setup for Local Development: ###
- Files & Data of Interest:
  - Dockerfile : main image definition and dependencies updates
  - docker-compose.yml : used for bring service up
  - db.sqlite3 : intially we publish local db to stash such that we have less conflicts
  - admin creds:
    - username: 'admin', password: 'password'

- Commands for local development: (needs to be run at root directory of app)
  - To start the application with all dependencies and Start the application development
  ```
  docker-compose up
  ```
  - If there is change in python dependencies and errors start coming in the terminal then we have to rebuild the images. Run these commands after you update ** requirements.txt ** with those extra dependencies. Normal sytax errors won't need this.
  ```
  docker rm -f $(docker ps -a -q) && docker rmi ccp-backend-brain_backend
  docker-compose up
  ``` 


  ### Api Documentation: ###
  - To See Available APIs: http://localhost:8000/openapi/

  - Checkout Swagger UI for APIs: http://localhost:8000/swagger-ui/