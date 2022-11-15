from flask import (
    Flask,
    render_template,
    request,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
import flask_login
import bcrypt
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(
    app,
    origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    supports_credentials=True,
)
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


class Ride(db.Model):
    __tablename__ = "ride"

    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String, db.ForeignKey("user.email"))

    departutre_adress_longitude = db.Column(db.Float)
    departutre_adress_latitude = db.Column(db.Float)
    arrival_adress_longitude = db.Column(db.Float)
    arrival_adress_latitude = db.Column(db.Float)
    departure_date_time = db.Column(db.DateTime)

    ride_is_started = db.Column(db.Boolean)
    ride_is_canceled = db.Column(db.Boolean)
    arrival_delay = db.Column(db.String, default="")  # Verspätungsspanne
    price_per_kilometer = db.Column(db.Float)
    type_of_car = db.Column(db.String)
    available_passenger_seats = db.Column(db.Integer)
    reserved_passenger_seats = db.Column(db.Integer)
    animal_free_car = db.Column(db.Boolean)
    corona_rules_in_car = db.Column(db.Boolean)
    smoking_in_car = db.Column(db.Boolean)

    user = db.relationship("User", foreign_keys=user_email, backref="rides")

    def get_ride_id(self):
        return self.ride_id

    def get_departure_adress(self):
        return self.departutre_adress

    def get_arrival_adress(self):
        return self.arrival_adress

    def is_started(self):
        return self.ride_is_started

    def is_canceled(self):
        return self.ride_is_canceled

    def get_price_per_kilometer(self):
        return self.price_per_kilometer

    def get_type_of_car(self):
        return self.type_of_car

    def get_free_passenger_seats(self):
        self.free_passenger_seats = (
            self.available_passenger_seats - self.reserved_passenger_seats
        )
        return self.free_passenger_seats

    def to_dict(self):
        return {
            "id": self.id,
            "departureAddress": self.departutre_adress,
            "arrivalAddress": self.arrival_adress,
            "departureDateTime": self.departure_date_time.isoformat(),
            "started": self.ride_is_started,
            "cancelled": self.ride_is_canceled,
            "arrivalDelay": self.arrival_delay,
            "pricePerKilometer": self.price_per_kilometer,
            "carType": self.type_of_car,
            "availableSeats": self.available_passenger_seats,
            "animalFree": self.animal_free_car,
            "coronaRules": self.corona_rules_in_car,
            "smoking": self.smoking_in_car,
        }


class Reservation(db.Model):
    __tablename__ = "reservation"

    user_email = db.Column(db.String, db.ForeignKey("user.email"), primary_key=True)
    ride_id = db.Column(db.Integer, db.ForeignKey("ride.id"), primary_key=True)

    user = db.relationship("User", foreign_keys=user_email, backref="reservations")
    ride = db.relationship("Ride", foreign_keys=ride_id, backref="reservations")


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
            return {"status": "success", "user": {"email": user.email}}
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


@app.route("/user-info", methods=["GET"])
@flask_login.login_required
def user_info():
    """Logout the current user."""
    user = flask_login.current_user
    mail = user.email
    print(user.__dir__())
    print(mail)
    return {"status": "success", "user": {"email": user.email}}


@app.route("/register", methods=["POST"])
def register():
    email = request.form["email"]
    password = request.form["password"]

    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()

    flask_login.login_user(user, remember=True)

    return {"status": "success"}


@app.route("/rides/posted", methods=["GET"])
def get_posted_rides():
    user = flask_login.current_user
    rides = user.rides
    return {"status": "success", "rides": [ride.to_dict() for ride in rides]}


@app.route("/rides/reserved", methods=["GET"])
def get_reserved_rides():
    user = flask_login.current_user
    rides = [reservation.ride for reservation in user.reservations]
    return {"status": "success", "rides": [ride.to_dict() for ride in rides]}


def create_mock_ride():
    return Ride(
        id=1,
        user_email="a@b.de",
        departutre_adress="Bonn",
        arrival_adress="GSO",
        departure_date_time=datetime.fromisoformat("2022-11-20T08:30:00+01:00"),
        ride_is_started=False,
        ride_is_canceled=False,
        arrival_delay="Verspätungsspanne",
        price_per_kilometer=1.23,
        type_of_car="Autotyp",
        available_passenger_seats=3,
        reserved_passenger_seats=1,
        animal_free_car=False,
        corona_rules_in_car=True,
        smoking_in_car=True,
    )


def create_mock_reservation():
    return Reservation(user_email="a@b.de", ride_id=1)


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
            ride = create_mock_ride()
            reservation = create_mock_reservation()
            db.session.add(user)
            db.session.add(ride)
            db.session.add(reservation)
            db.session.commit()
    app.run(debug=True)
