from flask import Flask, render_template, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import flask_login
import bcrypt
from flask_cors import CORS
from datetime import datetime, date, time, timedelta
import AdressConverter
from geopy.distance import geodesic as GD
import secrets
from base64 import b64decode
from SendMail import send_mail_from_template

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


@app.route("/images/<path:path>")
def send_report(path):
    return send_from_directory("images", path)


class UnverifiedUser(db.Model):
    email = db.Column(db.String, primary_key=True)
    auth_token = db.Column(db.String)


class PasswordResetRequest(db.Model):
    user_email = db.Column(db.String, db.ForeignKey("user.email"), primary_key=True)
    auth_token = db.Column(db.String)
    user = db.relationship(
        "User",
        foreign_keys=user_email,
        backref=db.backref("password_reset_requests"),
    )


class User(db.Model):
    __tablename__ = "user"

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    last_name = db.Column(db.String)
    first_name = db.Column(db.String)
    birthdate = db.Column(db.Date)
    gender = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)
    image = db.Column(db.String)
    type = db.Column(db.String)

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

    def to_dict(self):
        return {
            "email": self.email,
            "lastName": self.last_name,
            "firstName": self.first_name,
            "birthdate": self.birthdate.isoformat(),
            "gender": self.gender,
            "image": "images/" + self.image + ".png" if self.image else "",
            "type": self.type,
        }


class Ride(db.Model):
    __tablename__ = "ride"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String, db.ForeignKey("user.email"))

    address = db.Column(db.String)
    direction = db.Column(db.String)

    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    departure_date_time = db.Column(db.DateTime)

    ride_is_started = db.Column(db.Boolean, default=False)
    ride_is_canceled = db.Column(db.Boolean)
    delay_minutes = db.Column(db.Integer, nullable=True)
    price_per_kilometer = db.Column(db.Float)
    type_of_car = db.Column(db.String)
    available_passenger_seats = db.Column(db.Integer)
    reserved_passenger_seats = db.Column(db.Integer)
    pets = db.Column(db.Boolean)
    corona_hygiene = db.Column(db.Boolean, default=False)
    smoker = db.Column(db.Boolean, default=False)
    payment_cash = db.Column(db.Boolean, default=False)
    payment_paypal = db.Column(db.Boolean, default=False)

    user = db.relationship(
        "User",
        foreign_keys=user_email,
        backref=db.backref("rides", order_by=departure_date_time),
    )

    def get_remaining_seats(self):
        return self.available_passenger_seats - len(self.reservations)

    def to_dict(self, current_user):
        other = []
        if self.pets:
            other.append("pets")
        if self.corona_hygiene:
            other.append("coronaHygiene")
        if self.smoker:
            other.append("smoker")
        payment_methods = []
        if self.payment_cash:
            payment_methods.append("cash")
        if self.payment_paypal:
            payment_methods.append("paypal")
        return {
            "id": self.id,
            "address": self.address,
            "direction": self.direction,
            "departureDateTime": self.departure_date_time.isoformat(),
            "coordinates": {
                "latitude": self.latitude,
                "longitude": self.longitude,
            },
            "started": self.ride_is_started,
            "cancelled": self.ride_is_canceled,
            "pricePerKilometer": self.price_per_kilometer,
            "carType": self.type_of_car,
            "other": other,
            "availableSeats": self.available_passenger_seats,
            "remainingSeats": self.get_remaining_seats(),
            "isReserved": current_user.email
            in [r.user_email for r in self.reservations],
            "delayMinutes": self.delay_minutes,
            "userImage": "images/" + self.user.image + ".png"
            if self.user.image
            else "",
            "isOwner": self.user.email == current_user.email,
            "contactEmail": self.user.email,
            "isExpired": self.departure_date_time < datetime.now(),
            "ownerGender": self.user.gender,
            "reservations": [r.to_dict() for r in self.reservations],
            "isStarted": self.ride_is_started,
            "paymentMethods": payment_methods,
        }


class Reservation(db.Model):
    __tablename__ = "reservation"

    user_email = db.Column(db.String, db.ForeignKey("user.email"), primary_key=True)
    ride_id = db.Column(db.Integer, db.ForeignKey("ride.id"), primary_key=True)
    location = db.Column(db.String)

    ride = db.relationship("Ride", foreign_keys=ride_id, backref="reservations")
    user = db.relationship("User", foreign_keys=user_email, backref="reservations")

    def to_dict(self):
        return {"email": self.user_email, "location": self.location}

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
    return {"status": "success", "user": user.to_dict()}


@app.route("/reset-password", methods=["POST"])
def reset_password():
    email = request.json.get("email")

    # TODO: Send confirmation mail

    reset_request = PasswordResetRequest.query.get(email)
    if not reset_request:
        auth_token = secrets.token_urlsafe(32)
        reset_request = PasswordResetRequest(user_email=email, auth_token=auth_token)
        db.session.add(reset_request)
        db.session.commit()
        print("Created password reset request", reset_request, email, auth_token)
    else:
        print(
            "Re-using existing password reset request",
            reset_request,
            email,
            reset_request.auth_token,
        )

    send_mail_from_template(
        "passwortvergessen",
        email,
        link="http://127.0.0.1:5173/reset-password-confirm?token="
        + reset_request.auth_token,
    )

    return {"status": "success", "tempAuthToken": reset_request.auth_token}


def confirm_password_reset_token(token):
    return db.session.execute(
        db.select(PasswordResetRequest).filter_by(auth_token=token)
    ).scalar_one()


@app.route("/check-password-reset", methods=["GET"])
def check_password_reset():
    auth_token = request.args.get("token")
    reset_request = confirm_password_reset_token(auth_token)
    print(auth_token, reset_request)
    print(reset_request)
    if reset_request:
        print(reset_request.user_email)
        return {
            "status": "success",
            "email": reset_request.user_email,
            "token": auth_token,
        }
    else:
        return {"status", "fail"}, 403


@app.route("/reset-password-confirm", methods=["POST"])
def reset_password_confirm():
    auth_token = request.json.get("token")

    reset_request = confirm_password_reset_token(auth_token)

    user = reset_request.user
    print("Reset request user", user)

    user.password = bcrypt.hashpw(
        request.json.get("newPassword").encode("utf-8"), bcrypt.gensalt()
    )
    db.session.add(user)
    db.session.commit()

    return {"status": "success"}


@app.route("/register", methods=["POST"])
def register():
    email = request.json.get("email")

    # TODO: Send confirmation mail

    user = UnverifiedUser.query.get(email)
    if not user:
        auth_token = secrets.token_urlsafe(32)
        user = UnverifiedUser(email=email, auth_token=auth_token)
        db.session.add(user)
        db.session.commit()
        print("Created unverified user", user, email, auth_token)
    else:
        return {
            "status": "error",
            "message": "Benutzer mit dieser E-Mail Adresse existiert bereits",
        }, 409

    send_mail_from_template(
        "bestaetigungsmail",
        email,
        link="http://127.0.0.1:5173/register-confirm?token=" + user.auth_token,
    )

    return {"status": "success", "tempAuthToken": user.auth_token}


def confirm_register_token(token):
    return db.session.execute(
        db.select(UnverifiedUser).filter_by(auth_token=token)
    ).scalar_one()


@app.route("/check-registration", methods=["GET"])
def check_registration():
    auth_token = request.args.get("token")
    user = confirm_register_token(auth_token)
    print(auth_token, user)
    print(user)
    if user:
        print(user.email)
        return {"status": "success", "email": user.email, "token": auth_token}
    else:
        return {"status", "fail"}, 403


import re

teacher_email_regex = re.compile(r"^\w\.\w+@gso.schule.koeln$")


@app.route("/register-confirm", methods=["POST"])
def register_confirm():
    auth_token = request.json.get("token")

    unverified_user = confirm_register_token(auth_token)

    hashed_password = bcrypt.hashpw(
        request.json.get("password").encode("utf-8"), bcrypt.gensalt()
    )

    type = "student"
    if teacher_email_regex.match(unverified_user.email):
        type = "teacher"

    user = User(
        email=unverified_user.email,
        password=hashed_password,
        first_name=request.json.get("firstName"),
        last_name=request.json.get("lastName"),
        birthdate=date.fromisoformat(request.json.get("birthdate")),
        gender=request.json.get("gender"),
        type=type,
    )
    image_b64 = request.json.get("image")
    if image_b64:
        image_data = b64decode(image_b64)
        image_hash = secrets.token_hex()
        with open("images/" + image_hash + ".png", mode="wb") as f:
            f.write(image_data)
        user.image = image_hash
    db.session.add(user)
    db.session.commit()

    flask_login.login_user(user, remember=True)

    return {"status": "success", "user": user.to_dict()}


@app.route("/edit-user-details", methods=["POST"])
@flask_login.login_required
def edit_user_details():
    user = flask_login.current_user
    user.first_name = request.json.get("firstName")
    user.last_name = request.json.get("lastName")
    user.birthdate = date.fromisoformat(request.json.get("birthdate"))
    user.gender = request.json.get("gender")
    image_b64 = request.json.get("image")

    if image_b64:
        image_data = b64decode(image_b64)
        image_hash = secrets.token_hex()
        with open("images/" + image_hash + ".png", mode="wb") as f:
            f.write(image_data)
        user.image = image_hash

    new_password = request.json.get("newPassword")
    if new_password:
        user.password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())

    db.session.add(user)
    db.session.commit()

    return {"status": "success", "user": user.to_dict()}


@app.route("/rides/posted", methods=["GET"])
@flask_login.login_required
def get_posted_rides():
    user = flask_login.current_user
    rides = user.rides
    return {"status": "success", "rides": [ride.to_dict(user) for ride in rides]}


@app.route("/rides/detail", methods=["GET"])
@flask_login.login_required
def get_ride_detail():
    user = flask_login.current_user
    ride_id = request.args.get("id")

    ride = Ride.query.get(int(ride_id))
    return {"status": "success", "ride": ride.to_dict(user)}


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
    return {"status": "success", "rides": [ride.to_dict(user) for ride in rides]}


@app.route("/rides/reserve", methods=["POST"])
@flask_login.login_required
def reserve_ride():
    user = flask_login.current_user
    ride_id = int(request.json.get("id"))
    location = request.json.get("location")

    existing_reservation = (
        db.session.query(Reservation)
        .filter(
            (Reservation.user_email == user.email) & (Reservation.ride_id == ride_id)
        )
        .first()
    )

    if existing_reservation:
        return {"status": "fail", "message": "Reservierung existiert bereits"}

    ride = Ride.query.get(ride_id)
    reservation = Reservation(user_email=user.email, ride_id=ride_id, location=location)

    send_mail_from_template(
        "new_reservation",
        ride.user.email,
        date_time=ride.departure_date_time.strftime("%d.%m.%Y %H:%M"),
        link_to_details="http://127.0.0.1:5173/rides/detail/" + str(ride_id),
    )

    db.session.add(reservation)
    db.session.commit()

    return {"status": "success", "ride": reservation.ride.to_dict(user)}


@app.route("/rides/start", methods=["POST"])
@flask_login.login_required
def start_ride():
    user = flask_login.current_user
    ride_id = int(request.json.get("id"))

    ride = Ride.query.get(ride_id)
    ride.ride_is_started = True
    db.session.add(ride)
    db.session.commit()

    return {"status": "success", "ride": ride.to_dict(user)}


@app.route("/rides/cancel", methods=["POST"])
@flask_login.login_required
def cancel_ride():
    ride_id = int(request.json.get("id"))

    ride = Ride.query.get(ride_id)

    if not ride:
        return {"status": "fail", "message": "Fahrt existiert nicht"}

    for reservation in ride.reservations:
        send_mail_from_template(
            "user_canceled_ride",
            reservation.user_email,
            date_time=ride.departure_date_time.strftime("%d.%m.%Y %H:%M"),
        )
        db.session.delete(reservation)

    db.session.delete(ride)
    db.session.commit()

    return {"status": "success"}


@app.route("/rides/cancel-reservation", methods=["POST"])
@flask_login.login_required
def cancel_reservation():
    user = flask_login.current_user
    ride_id = int(request.json.get("id"))

    existing_reservation = (
        db.session.query(Reservation)
        .filter(
            (Reservation.user_email == user.email) & (Reservation.ride_id == ride_id)
        )
        .first()
    )

    if not existing_reservation:
        return {"status": "fail", "message": "Reservierung existiert nicht"}

    ride = existing_reservation.ride

    send_mail_from_template(
        "canceled_reservation",
        ride.user.email,
        date_time=ride.departure_date_time.strftime("%d.%m.%Y %H:%M"),
        link_to_details="http://127.0.0.1:5173/rides/detail/" + str(ride.id),
    )

    db.session.delete(existing_reservation)
    db.session.commit()

    return {"status": "success", "ride": ride.to_dict(user)}


@app.route("/rides/report-delay", methods=["POST"])
@flask_login.login_required
def report_delay():
    user = flask_login.current_user

    ride = Ride.query.get(request.json.get("id"))
    ride.delay_minutes = request.json.get("delayMinutes")

    for reservation in ride.reservations:
        email = reservation.user_email
        send_mail_from_template(
            "verspaetung",
            email,
            date_time=ride.departure_date_time.strftime("%d.%m.%Y %H:%M"),
            delay=ride.delay_minutes,
        )

    db.session.add(ride)
    db.session.commit()
    return {"status": "success", "ride": ride.to_dict(user)}


@app.route("/rides/create", methods=["POST"])
@flask_login.login_required
def create_ride():
    user = flask_login.current_user
    address = request.json.get("address")
    direction = request.json.get("direction")

    coordinates, place_name = AdressConverter.get_mapbox_coordinates(address)

    other = request.json.get("other")
    payment_methods = request.json.get("paymentMethods")

    ride = Ride(
        user_email=user.email,
        address=place_name,
        direction=direction,
        latitude=coordinates["latitude"],
        longitude=coordinates["longitude"],
        departure_date_time=datetime.fromisoformat(
            request.json.get("departureDateTime")
        ),
        ride_is_started=False,
        ride_is_canceled=False,
        price_per_kilometer=request.json.get("pricePerKilometer"),
        type_of_car=request.json.get("carType"),
        available_passenger_seats=request.json.get("availableSeatCount"),
        pets="pets" in other,
        corona_hygiene="coronaHygiene" in other,
        smoker="smoker" in other,
        payment_cash="cash" in payment_methods,
        payment_paypal="paypal" in payment_methods,
    )
    db.session.add(ride)
    db.session.commit()
    return {"status": "success", "ride": ride.to_dict(user)}


@app.route("/rides/search", methods=["GET"])
@flask_login.login_required
def search_rides():
    user = flask_login.current_user
    print(request.args)
    the_date = date.fromisoformat(request.args.get("date"))
    time_start = time.fromisoformat(request.args.get("timeRangeStart"))
    time_end = time.fromisoformat(request.args.get("timeRangeEnd"))
    start_range = datetime.combine(the_date, time_start)
    end_range = datetime.combine(the_date, time_end)
    direction = request.args.get("direction")
    payment_methods = request.args.get("paymentMethods")

    max_price_per_kilometer = request.args.get("pricePerKilometer")
    max_distance_km = float(request.args.get("maxDistance"))

    input_place_name = request.args.get("address")
    coordinates, place_name = AdressConverter.get_mapbox_coordinates(input_place_name)

    other = request.args.get("other")

    print("in", coordinates, place_name)

    # rides = (
    #     db.session.query(Ride)
    #     .join(User)
    #     .filter(Ride.user_email == user.email)
    #     .order_by(Ride.departure_date_time)
    #     .all()
    # )

    rides_query = Ride.query.filter(
        (Ride.departure_date_time >= start_range)
        & (Ride.departure_date_time <= end_range)
        & (Ride.direction == direction)
        & (Ride.user.has(type=user.type))
        & (Ride.price_per_kilometer <= max_price_per_kilometer)
    )
    if "coronaHygiene" in other:
        rides_query = rides_query.filter(Ride.corona_hygiene == True)
    if not "smoker" in other:
        rides_query = rides_query.filter(Ride.smoker == False)
    if not "pets" in other:
        rides_query = rides_query.filter(Ride.pets == False)

    if "cash" in payment_methods and "paypal" in payment_methods:
        rides_query = rides_query.filter(
            (Ride.payment_cash == True) | (Ride.payment_paypal == True)
        )
    elif "cash" in payment_methods:
        rides_query = rides_query.filter(Ride.payment_cash == True)
    elif "paypal" in payment_methods:
        rides_query = rides_query.filter(Ride.payment_paypal == True)

    rides = rides_query.all()

    rides = [r for r in rides if r.get_remaining_seats() > 0]

    ride_distances = {}
    for ride in rides:
        ride_distances[ride.id] = GD(
            (ride.latitude, ride.longitude),
            (coordinates["latitude"], coordinates["longitude"]),
        )
        print(ride, ride_distances[ride.id])

    sorted_rides = sorted(rides, key=lambda ride: ride_distances[ride.id].meters)

    sorted_filtered_rides = [
        r for r in sorted_rides if ride_distances[ride.id].km <= max_distance_km
    ]

    ride_dicts = [
        ride.to_dict(user) | {"distance": ride_distances[ride.id].meters}
        for ride in sorted_filtered_rides
    ]

    return {"status": "success", "rides": ride_dicts}


def create_mock_ride(label, date_time, lat, long):
    return Ride(
        user_email="a@b.de",
        address=label,
        direction=random.choice(["from", "to"]),
        longitude=long,
        latitude=lat,
        departure_date_time=date_time,
        ride_is_started=False,
        ride_is_canceled=False,
        delay_minutes=random.randrange(0, 30),
        price_per_kilometer=1.23,
        type_of_car="Autotyp",
        available_passenger_seats=1,
        pets=False,
        corona_hygiene=True,
        smoker=True,
        payment_cash=True,
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
            user1 = User(
                email="a@b.de",
                first_name="Test",
                last_name="Account",
                password=bcrypt.hashpw("123".encode("utf-8"), bcrypt.gensalt()),
                birthdate=date.fromisoformat("2000-01-01"),
                type="student",
                gender="männlich",
            )
            user2 = User(
                email="b@c.de",
                first_name="Test2",
                last_name="Account2",
                password=bcrypt.hashpw("123".encode("utf-8"), bcrypt.gensalt()),
                birthdate=date.fromisoformat("2000-01-02"),
                type="student",
                gender="weiblich",
            )
            user3 = User(
                email="teacher1@c.de",
                first_name="Test2",
                last_name="Account2",
                password=bcrypt.hashpw("123".encode("utf-8"), bcrypt.gensalt()),
                birthdate=date.fromisoformat("2000-01-02"),
                type="teacher",
                gender="männlich",
            )
            user4 = User(
                email="teacher2@c.de",
                first_name="Test2",
                last_name="Account2",
                password=bcrypt.hashpw("123".encode("utf-8"), bcrypt.gensalt()),
                birthdate=date.fromisoformat("2000-01-02"),
                type="teacher",
                gender="männlich",
            )
            db.session.add(user1)
            db.session.add(user2)
            db.session.add(user3)
            db.session.add(user4)
            start_date_time = datetime.fromisoformat("2022-11-17T08:30:00+01:00")
            for x in range(10):
                coordinates, place_name = random.choice(resolved_places)
                ride = create_mock_ride(
                    place_name,
                    start_date_time,
                    coordinates["latitude"],
                    coordinates["longitude"],
                )
                db.session.add(ride)
                start_date_time += timedelta(hours=8)
            db.session.commit()
    app.run(debug=True)
