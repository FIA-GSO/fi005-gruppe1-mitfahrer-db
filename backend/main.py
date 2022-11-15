from flask import (
    Flask,
    render_template,
    request,
)
from flask_sqlalchemy import SQLAlchemy
import flask_login
import bcrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.secret_key = "super secret string"  # Change this!
db = SQLAlchemy(app)
db.init_app(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(db.Model):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """

    __tablename__ = "user"

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    last_name = db.Column(db.String)
    first_name = db.Column(db.String)
    birthdate = db.Column(db.Date)
    gender = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id)


@app.route("/login", methods=["POST"])
def login():
    """For GET requests, display the login form.
    For POSTS, login the current user by processing the form.

    """
    print("js", request.json)
    user = User.query.get(request.json.get("email"))
    print(user)
    if user:
        if bcrypt.checkpw(request.json.get("password").encode("utf-8"), user.password):
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            flask_login.login_user(user, remember=True)
            return {"status": "success"}
    return {"status": "fail"}, 403


@app.route("/logout", methods=["GET"])
@flask_login.login_required
def logout():
    """Logout the current user."""
    user = flask_login.current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    flask_login.logout_user()
    return {"status": "success"}


@app.route("/register", methods=["POST"])
def register():
    email = request.form["email"]
    password = request.form["password"]

    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()

    flask_login.login_user(user, remember=True)

    return {"status": "success"}


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if not User.query.get("a@b.de"):
            print("creating user")
            email = "a@b.de"
            password = "123"
            user = User(
                email=email,
                password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()),
            )
            db.session.add(user)
            db.session.commit()
    app.run(debug=True)
