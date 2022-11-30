"""Setup at app startup"""
import os
import sqlalchemy
from flask import Flask, session, g
from yaml import load, Loader



def init_connection_engine():
    """ initialize database setup
    Takes in os variables from environment if on GCP
    Reads in local variables that will be ignored in public repository.
    Returns:
        pool -- a connection to GCP MySQL
    """


    # detect env local or gcp
    if os.environ.get('GAE_ENV') != 'standard':
        try:
            variables = load(open("app.yaml"), Loader=Loader)
        except OSError as e:
            print("Make sure you have the app.yaml file setup")
            os.exit()

        env_variables = variables['env_variables']
        try:
            for var in env_variables:
                os.environ[var] = env_variables[var]
        except TypeError as e:
            print("error", var)
            raise e

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            database=os.environ.get('MYSQL_DB'),
            host=os.environ.get('MYSQL_HOST')
        )
    )

    return pool


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.before_request
def my_before_request():
    userid = session.get("userid")
    if userid:
        #user = db_helper.search_user(userid)
        setattr(g, "user", userid)
    else:
        setattr(g, "user", None)

@app.context_processor
def my_context_processor():
    return {"user": g.user}

db = init_connection_engine()

# conn = db.connect()
# results = conn.execute("Select * from Company")
# # we do this because results is an object, this is just a quick way to verify the content
# print([x for x in results])
# conn.close()

# To prevent from using a blueprint, we use a cyclic import
# This also means that we need to place this import here
# pylint: disable=cyclic-import, wrong-import-position
from app import routes
