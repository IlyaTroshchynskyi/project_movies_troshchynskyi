# -*- coding: utf-8 -*-
"""
    Module register cli command
"""

from flask.cli import FlaskGroup
from app import app
from movies import db
from movies.insert_data import populate_db

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    """
    Create database tables
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("populate_data")
def insert_data():
    """
    Populate db by test data
    """
    populate_db()


if __name__ == "__main__":
    cli()
