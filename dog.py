from flask_migrate import Migrate

from application.app import create_app
from application.ext import db
from application.model import *

app = create_app()

Migrate(app, db)


@app.cli.command()
def hello():
    print('hello')
