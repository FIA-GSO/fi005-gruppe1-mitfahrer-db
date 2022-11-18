from server import app, db
from .entities import Reservation, Ride
from flask import request
import flask_login
from lib.SendMail import send_mail_from_template
from geopy.distance import geodesic as GD
import lib.AdressConverter as AdressConverter
from datetime import datetime, date, time


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
