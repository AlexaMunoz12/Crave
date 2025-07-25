# Crave
---
## Installation:

First create a python virtual environment

`python -m venv .venv`

Then activate the virtual environment

`source .venv/bin/active`

Install dependencies

`pip install -r requirements.txt`

In the root directory of the project `Crave/` initialize the database by running

`flask --app flaskr init-db`

Then to run the app

`flask --app flaskr run --debug`