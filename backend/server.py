from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_login
from flask_cors import CORS

app = Flask(__name__)
CORS(
    app,
    origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    supports_credentials=True,
)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.secret_key = "super secret string"
db = SQLAlchemy(app)
db.init_app(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
