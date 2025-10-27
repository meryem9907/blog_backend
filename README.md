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


