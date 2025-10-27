# Django blog api with REST endpoints

This is simple django blog api with following basic features:
- create author
- post texts
- add tags to posts
- comment posts

## Run in development mode
- Prereq:
    - Python 3.13
- clone the project
- direct to your project folder
- install requirements
`pip install -r requirements.txt`
- create and activate a virtual environment
`pipenv shell`
- create migrations and run them. Afterwards run the server:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Doc endpoints
Api documentation can be viewed on following endpoints:
- /api/docs/swagger/
- /api/docs/redoc/


## Deployment via docker


