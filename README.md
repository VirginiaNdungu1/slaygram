# slaygram
A simple, fun and creative way to capture and share photos with friends and family

## Prerequisites
    confusable-homoglyphs==2.0.2
    Django==1.11.7
    django-bootstrap3==9.1.0
    django-likes==1.11
    django-registration==2.3
    django-secretballot==0.7.1
    django-tinymce==2.6.0
    django-vote==2.1.5
    olefile==0.44
    Pillow==4.3.0
    psycopg2==2.7.3.2
    pytz==2017.3
    votes==1.0.1


## Installation

* `git clone <repository-url>` this repository
* `cd slaygram`


## Project Specifications

    Features
     As a User, i should be able to:
        Create an account with slaygram
        Login to Slay gram
        View posts on my profile
        Access my timeline
        Follow other users on slaygram
        View my 'following' user's posts on my timeline
        search for a user
        Like a post
        Comment on post
        Save it on my machine



## Known Bugs
Copy image link of the image does not work properly

## Running / Development

python manage.py runserver

Running on http://127.0.0.1:8000/

## Hosting / Production

      ### requirements
            gunicorn==19.7.1
            python-decouple==3.1
            whitenoise==3.3.1
            dj-database-url==0.4.2


### Running Tests

      python3.6 manage.py test

## Technologies Used
       Python3.6
       django
       Postgres Database
       Bootstrap
       CSS
       HTML

    Deployment:
       Heroku


Copyright (c) 2017 Virginia Ndung'u
