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

### Run tests
`python manage.py test`
- alternatively you can use the curl endpoints in tests.sh. Make sure you run the server before that.
    - Note before running the script:
          - Flush the database with `python manage.py flush`
          - install jq
          - run in an bash environment 

## Deployment via docker
- Install docker on https://docs.docker.com/get-started/get-docker/
- Build the container
`docker build -t blog-api .`
- Check if container runs
`docker image list`
- Run server via
```
# ensure in settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        "OPTIONS": {"timeout": 20}
    }
}
# create volume an run api via docker
docker volume create blog_db
docker run --name blog-api -p 8000:8000 --env-file .env -v blog_db:/app/data blog-api
```
- Server is available at: http://127.0.0.1:8000


## Current database
- the default database used is the file-based sql-lite database


