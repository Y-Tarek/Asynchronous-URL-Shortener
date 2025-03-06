# Asynchronous URL Shortener.
URL shortener application that allows users to shorten long URLs and retrieve the
original URL using the shortened link.

## API Postman Documentation
https://documenter.getpostman.com/view/28439113/2sAYdmmoV9

## Prerequisite
>python

>redis (optional-if you wish to run locally)


## Installtion & Running Set Up Virtual Environment:

        - For Redis installation:
            On Ubuntu/Debian: 
            Use the following commands to install Redis:
                  1- sudo apt update
                  2- sudo apt install redis -y
            On macos:
               1-  brew install redis
               2- brew services start redis

            On windows:
               You can download the Redis binaries from the Redis website or use the Windows Subsystem for Linux (WSL) to install Redis.
               
        - python -m venv venv.
              source venv/bin/activate  (Linux venv activation)
              venv/scripts/activate     (Windows venv activation)
            
         - Install Dependencies:: 
             pip install -r requirememnts.txt.
             
         - Apply Migrations:
             python manage.py migrate.

         - Start redis server
               redis-server

          - Run Celery
              celery -A valify_task worker --loglevel=info

          - Run the Development Server:
               python manage.py runserver
               The server will be available at http://127.0.0.1:8000. Use the API documentation above to test APIs,
               
          - Run Tests:
              python manage.py test

## Runing Using Docker

       - The Application is dockerized and can run with running this command:
            docker compose up --build
            The server will be available at http://0.0.0.0:8000. Use the API documentation above to test APIs,
            
            
