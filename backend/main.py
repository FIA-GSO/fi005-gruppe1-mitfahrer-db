from flask import (
    Flask,
    render_template,
    request,
)
from flask_sqlalchemy import SQLAlchemy
import flask_login
import bcrypt
from flask_cors import CORS
from datetime import datetime, date, time, timedelta
import AdressConverter
from geopy.distance import geodesic as GD

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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String, db.ForeignKey("user.email"))

    departutre_adress = db.Column(db.String)

    departutre_adress_longitude = db.Column(db.Float)
    departutre_adress_latitude = db.Column(db.Float)
    arrival_adress_longitude = db.Column(db.Float)
    arrival_adress_latitude = db.Column(db.Float)

    arrival_adress = db.Column(db.String)
    departure_date_time = db.Column(db.DateTime)

    ride_is_started = db.Column(db.Boolean)
    ride_is_canceled = db.Column(db.Boolean)
    arrival_delay = db.Column(db.String, default="", nullable=True)  # Verspätungsspanne
    price_per_kilometer = db.Column(db.Float)
    type_of_car = db.Column(db.String)
    available_passenger_seats = db.Column(db.Integer)
    reserved_passenger_seats = db.Column(db.Integer)
    animal_free_car = db.Column(db.Boolean)
    corona_rules_in_car = db.Column(db.Boolean)
    smoking_in_car = db.Column(db.Boolean)

    user = db.relationship(
        "User",
        foreign_keys=user_email,
        backref=db.backref("rides", order_by=departure_date_time),
    )

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
            "departureCoordinates": {
                "latitude": self.departutre_adress_latitude,
                "longitude": self.departutre_adress_longitude,
            },
            "arrivalCoordinates": {
                "latitude": self.arrival_adress_latitude,
                "longitude": self.arrival_adress_longitude,
            },
            "started": self.ride_is_started,
            "cancelled": self.ride_is_canceled,
            "arrivalDelay": self.arrival_delay,
            "pricePerKilometer": self.price_per_kilometer,
            "carType": self.type_of_car,
            "availableSeats": self.available_passenger_seats,
            "animalFree": self.animal_free_car,
            "coronaRules": self.corona_rules_in_car,
            "smoking": self.smoking_in_car,
            "remainingSeats": self.available_passenger_seats - len(self.reservations),
        }


class Reservation(db.Model):
    __tablename__ = "reservation"

    user_email = db.Column(db.String, db.ForeignKey("user.email"), primary_key=True)
    ride_id = db.Column(db.Integer, db.ForeignKey("ride.id"), primary_key=True)

    ride = db.relationship("Ride", foreign_keys=ride_id, backref="reservations")
    user = db.relationship("User", foreign_keys=user_email, backref="reservations")

    # user = db.relationship("User", foreign_keys=user_email, backref="reservations")


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
@flask_login.login_required
def get_posted_rides():
    user = flask_login.current_user
    rides = user.rides
    return {"status": "success", "rides": [ride.to_dict() for ride in rides]}


@app.route("/rides/reserved", methods=["GET"])
@flask_login.login_required
def get_reserved_rides():

    user = flask_login.current_user

    reservations = (
        db.session.query(Reservation)
        .join(Ride)
        .filter(Reservation.user_email == user.email)
        .order_by(Ride.departure_date_time)
        .all()
    )

    for reservation in reservations:
        print(reservation.ride)

    rides = [reservation.ride for reservation in reservations]
    return {"status": "success", "rides": [ride.to_dict() for ride in rides]}


@app.route("/rides/create", methods=["POST"])
@flask_login.login_required
def create_ride():

    departutre_adress = request.json.get("departureAddress")
    arrival_adress = request.json.get("arrivalAddress")

    (
        departure_coordinates,
        departure_place_name,
    ) = AdressConverter.get_mapbox_coordinates(departutre_adress)
    arrival_coordinates, arrival_place_name = AdressConverter.get_mapbox_coordinates(
        arrival_adress
    )

    other = request.json.get("other")
    ride = Ride(
        user_email=flask_login.current_user.email,
        departutre_adress=departure_place_name,
        arrival_adress=arrival_place_name,
        departure_date_time=datetime.fromisoformat(
            request.json.get("departureDateTime")
        ),
        departutre_adress_longitude=departure_coordinates["longitude"],
        departutre_adress_latitude=departure_coordinates["latitude"],
        arrival_adress_longitude=arrival_coordinates["longitude"],
        arrival_adress_latitude=arrival_coordinates["latitude"],
        ride_is_started=False,
        ride_is_canceled=False,
        arrival_delay="",
        price_per_kilometer=request.json.get("pricePerKilometer"),
        type_of_car=request.json.get("carType"),
        available_passenger_seats=request.json.get("availableSeatCount"),
        reserved_passenger_seats=0,
        animal_free_car="pets" in other,
        corona_rules_in_car="coronaHygiene" in other,
        smoking_in_car="smoking" in other,
    )
    db.session.add(ride)
    db.session.commit()
    return {"status": "success", "ride": ride.to_dict()}


@app.route("/rides/search", methods=["GET"])
@flask_login.login_required
def search_rides():
    print(request.args)
    the_date = date.fromisoformat(request.args.get("date"))
    time_start = time.fromisoformat(request.args.get("timeRangeStart"))
    time_end = time.fromisoformat(request.args.get("timeRangeEnd"))
    start_range = datetime.combine(the_date, time_start)
    end_range = datetime.combine(the_date, time_end)

    input_place_name = request.args.get("placeName")
    coordinates, place_name = AdressConverter.get_mapbox_coordinates(input_place_name)

    print("in", coordinates, place_name)

    rides = Ride.query.filter(
        (Ride.departure_date_time >= start_range)
        & (Ride.departure_date_time <= end_range)
    ).all()

    ride_distances = {}
    for ride in rides:
        ride_distances[ride.id] = GD(
            (ride.departutre_adress_latitude, ride.departutre_adress_longitude),
            (coordinates["latitude"], coordinates["longitude"]),
        )
        print(ride, ride_distances[ride.id])

    sorted_rides = sorted(rides, key=lambda ride: ride_distances[ride.id].meters)

    ride_dicts = [
        ride.to_dict() | {"distance": ride_distances[ride.id].meters}
        for ride in sorted_rides
    ]

    return {"status": "success", "rides": ride_dicts}


def create_mock_ride(label, date_time, lat, long):
    return Ride(
        user_email="a@b.de",
        departutre_adress=label,
        departutre_adress_longitude=long,
        departutre_adress_latitude=lat,
        arrival_adress=label,
        departure_date_time=date_time,
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


def create_mock_reservation2():
    return Reservation(user_email="a@b.de", ride_id=2)


@app.route("/")
def index():
    return render_template("index.html")


resolved_places = [
    (
        {"latitude": 50.9426125, "longitude": 6.9585985},
        "Köln Hauptbahnhof, Trankgasse 11, Köln, Nordrhein-Westfalen 50667, Deutschland",
    ),
    (
        {"latitude": 50.93641065, "longitude": 6.99835925},
        "Trimbornstraße, 51105 Köln, Deutschland",
    ),
    (
        {"latitude": 50.9355132, "longitude": 6.9386099},
        "Habsburgerring, 50674 Köln, Deutschland",
    ),
    (
        {"latitude": 50.936625, "longitude": 6.94858},
        "Neumarkt Galerie, Neumarkt 2-4, Köln, Nordrhein-Westfalen 50667, Deutschland",
    ),
]

import random

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if not User.query.get("a@b.de"):
            print("creating database")
            email = "a@b.de"
            password = "123"
            user = User(
                email=email,
                password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()),
            )
            db.session.add(user)
            start_date_time = datetime.fromisoformat("2022-11-20T08:30:00+01:00")
            for x in range(20):
                coordinates, place_name = random.choice(resolved_places)
                ride = create_mock_ride(
                    place_name,
                    start_date_time,
                    coordinates["latitude"],
                    coordinates["longitude"],
                )
                db.session.add(ride)
                start_date_time += timedelta(minutes=15)
            db.session.commit()
    app.run(debug=True)
