import os

from dotenv import load_dotenv
from flask import Flask
from flask_wtf.csrf import CSRFProtect

load_dotenv()

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

from Curative import routes
