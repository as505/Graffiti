import sqlite3
from flask import current_app, g
from datetime import datetime
import click
from pathlib import Path

DATABASE = 'database.db'

def get_database():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def close_database(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_database():
    # reset database
    open(DATABASE, 'w').close()

    db = get_database()

    with current_app.open_resource('schema.sql') as file:
        db.executescript(file.read().decode('utf8'))


@click.command('init_db')
def init_db_command():
    init_database()
    click.echo('Database initialized successfully')


sqlite3.register_converter(
    'timestamp', lambda v: datetime.fromisoformat(v.decode())
)


def init_app(app):
    app.teardown_appcontext(close_database)
    app.cli.add_command(init_db_command)