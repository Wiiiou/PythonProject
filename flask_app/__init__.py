# __init__.py
from flask import Flask
app = Flask(__name__, static_url_path='/static')
app.secret_key = "dragons"
database="python_project_db"