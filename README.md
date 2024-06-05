## Starting out!
Make sure you have Python3 installed on your system.
All the following commands must be executed inside our project's root directory.

Run `python3 -m venv venv` to create the project's virtual environment.

In case VS Code still isn't using our virtual envrionment's Python interpreter, open VSCode's command palette (`cmd+shift+p` on macOS) and select "Select Python Interpreter" then "Enter interpreter path" and input the path manually like so `./venv/bin/python`.

Run bash script `source venv/bin/activate` so that when you use `pip install` to install new Python packages it only installs in our project's virtual environment, and not the global environemnt on our machine.

## Required packages:

Once you activate the project's virtual environment, youl'll need to `pip install` the following:

`pip install fastapi`
`pip install psycopg2-binary`
`pip install sqlalchemy`
`pip install 'passlib[bcrypt]'`
`pip install 'python-jose[cryptography]'`
`pip install pydantic-settings`

Run `pip freeeze` to check that all the aforementioned packages were installed.

Download and install PostgreSQL, host a database on localhost and connect to it by providing its credentials in the project.

Create .env file in the project's root directory with the following keys and values according to database configurations:
DATABASE_HOSTNAME=localhost // database host name
DATABASE_PORT=5432 // database host port
DATABASE_PASSWORD=password // database host port
DATABASE_NAME=fastapi-todo // database name
DATABASE_USERNAME=postgres // database password
SECRET_KEY=any random number  // run `openssl rand -hex 32` to generate a long random key for jwt signing
ALGORITHM=HS256 // we'll use HMAC SHA256
ACCESS_TOKEN_EXPIRE_MINUTES=30 // set jwt acccess token lifetime to 30 mins

## Not required but recommended:

Download and install Postman to test the backend's endpoints, you can also test with `curl`, or use http://localhost:port/docs or http://localhost:port/redoc that FastAPI already provides.


## Last but not least..

Run `uvicorn app.main:app --reload` to see the magic in action :)