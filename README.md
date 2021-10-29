# Softdesk API Documentation
## Table of contents
1. [General Informations](#general-info)
2. [Technologies](#technologies)
3. [Installation](#installation)

### General Informations
***
API Documentation for the Softdesk Application, follow the instructions to properly setup the api and launch the http requests. 
The Softdesk API is organized around REST. This API has predictable resource-oriented URLs, accepts JSON request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.
### Screenshot
![Image text](https://i.ibb.co/LC80vpd/banniere-op.png)
## Technologies
***
Librairies used :
* [Python 64bit](https://www.python.org/downloads/release/python-391/): Version 3.9.1
* [Django](https://www.djangoproject.com/)
* [djangorestframework](https://www.django-rest-framework.org/)
* [drf-nested-routers](https://github.com/alanjds/drf-nested-routers)
* [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)

## Installation
***
To use the API and make the HTTP requests :

```
On Windows : 
$ git clone https://github.com/VictorTherache/P10-Softdesk-API.git
$ cd P10-Softdesk-API
```
Activate your virtual environement : 
```
$ pip install virtualenv
$ .\env\Scripts\activate
```
Then : 
```
$ pip3 install -r requirements.txt 
$ cd .\medium_api\
$ python manage.py makemigrations api
$ python manage.py migrate
$ python manage.py runserver
```
```
On Linux/Mac : 
$ git clone https://github.com/VictorTherache/P10-Softdesk-API.git
$ cd P10-Softdesk-API
$ source env/bin/activate
$ pip3 install -r requirements.txt 
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

