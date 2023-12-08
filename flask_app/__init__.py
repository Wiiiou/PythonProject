# __init__.py
from flask import Flask
# <<<<<<< HEAD
app = Flask(__name__)
# =======
app = Flask(__name__, static_url_path='/static')
# >>>>>>> 3c405feca521acac7982812b67228e6b14a27fc2
app.secret_key = "dragons"
database="python_project_db"