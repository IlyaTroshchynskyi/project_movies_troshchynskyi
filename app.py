# -*- coding: utf-8 -*-
"""
    The entry point WSGI application object.
"""

from movies import create_app
from movies.config import Configuration

app = create_app(Configuration)

if __name__ == "__main__":
    app.run(debug=True)
