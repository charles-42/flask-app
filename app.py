#! /usr/bin/env python
from venv import create
from my_app import create_app
from dotenv import load_dotenv
import os

load_dotenv(override=True)

MODE = os.environ.get('MODE')

app = create_app(MODE)

if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port=8000)