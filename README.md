# Mailing Service

## Description
This mailing service allows users to send mailings about their products to a large number of customers. The service includes a server part for working with the database and a front-end part.
## Installation
Firstly install the project from GitHub and place it somewhere easily accessible from your driver, for example if your drive is named C:, then the location should be something like:
```
C:\MailingService\
```
This should clone this project from Github:
```
git clone https://github.com/IgorSorokin1985/CW6_mailing_of_letters.git
```
Remember to go into the folder that the service is in. Then to install required libraries and frameworks run the commands:
```
pip install -r requirements.txt
```
When that is said and done, that should be it on the computer side, you should connect this service with Database.

## Database connection
You should install PosgreSQL. 
```
https://www.postgresql.org/download/
```

Then create Database.
```
CREATE DATABASE mailing_database
```
Then it is need connect service with Database. You need to specify the database parameters in the file "config/settings.py" (user and password for example).
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mailing_database',
        'USER': 'postgres',
        'PASSWORD': '1234',
    }
}
```

## Environment variables
## Loading data
## Creating a superuser
## Creating a user
## User verification
## Group of staff users
## Moderator capabilities
## Content manager capabilities
## Start schedule
## Additional commands
