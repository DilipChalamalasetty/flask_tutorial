import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

# used to create the connection to the database
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# used to close the connection to the database

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# call get_db()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# @click.command('init-db')
# @with_appcontext
# def init_db_command():
#     """Clear the existing data and create new tables."""
#     init_db()
#     click.echo('Initialized the database.')

# teardown_appcontext() will excute the set of function at the ending
def init_app(app):
    app.teardown_appcontext(close_db)
    # app.cli.add_command(init_db_command)
    init_db()

