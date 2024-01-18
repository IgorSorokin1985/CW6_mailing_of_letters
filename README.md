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
Then you should make migrations with these commands
```
python manage.py makemigrations
```
If all is ok then
```
python manage.py migrate
```

## Environment variables
For working Mailing service it is need create file ".env" with information about your email service and other. Example this file you can see as ".env.sample"
```
EMAIL_HOST=
EMAIL=
EMAIL_PASSWORD=
CACHE_ENABLED=
CACHE_LOCATION=
```

## Creating a superuser
For creating superuser you should use command
```
pyton manage.py csu
```

## Group of staff users
There are two groups for staff users - **Moderator** and **Content Manager**.
Only Superuser can add permission in admin panel.

## Moderator capabilities
Moderator can view all mailings and users. Moderator can cancel and activate all mailings. Moderator can deactivate and activate all users. Moderator cannot change and delete mailings.

## Content manager capabilities
Content manager can add and change articles.

## Start schedule
For starting automatic sending mailings you should use command. Apscheduler look all mailings, check which mailings should be sended and send. This checking happens every 10 seconds.
```
pyton manage.py runapscheduler
```

## Other commands
For onetime sending all ready mailings you should use command
```
pyton manage.py runmailings
```