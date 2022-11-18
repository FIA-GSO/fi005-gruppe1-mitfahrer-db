from server import db
from datetime import datetime


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
