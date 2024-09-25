# Move into your project folder

->cd project

# Install and activate your virtual environment

-> pip install virtualenv
-> virtualenv venv
-> python -m venv venv
-> venv\Scripts\activate.bat (for Windows PC)

# Install all dependencies and verify

-> pip install -r requirements.txt
-> pip list

# Store sensitive info in .env file created in root of the project folder and install this package

pip install python-decouple

store db info like this in .env file:

    DATABASE_NAME=mydatabase
    DATABASE_USER=myuser
    DATABASE_PASSWORD=mypassword

In settings.py use abiove veriable as below:

from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Move into the cloned repository and run below commands

set up your db connection in settings.py
python manage.py makemigrations
pythion manage.py migrate
python manage.py createsuperuser
python manage.py runserver





