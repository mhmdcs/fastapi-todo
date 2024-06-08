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

`pip install pytest`

Run `pip freeze` to check that all the aforementioned packages were installed.

Or, simply just run `pip install -r requirements.txt` and it'll install all the needed packages for you.

Download and install PostgreSQL, host a database on localhost and connect to it by providing its credentials in the project.

Create .env file in the project's root directory with the following keys and values according to database configurations:

```
DATABASE_CONNECTION_STRING=postgresql://postgres:password@localhost:port/database-name
SECRET_KEY=any random number  // run `openssl rand -hex 32` to generate a long random key for jwt signing
```

## Not required but recommended:

Download and install Postman to test the backend's endpoints, you can also test with `curl`, or use http://localhost:port/docs or http://localhost:port/redoc that FastAPI already provides.

## Optional: Run the tests
If you have installed `pytest`, which you should if you installed the required dependencies/modules/packages via `pip install -r requirements.txt`, then you can run all the tests written in the `tests` directory via running `pytest --disable-warnings -vx` from the project's root directory.

## Last but not least..

Run `uvicorn app.main:app --reload` to see the magic in action :)