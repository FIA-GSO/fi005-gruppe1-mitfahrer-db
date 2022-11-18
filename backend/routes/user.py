from server import app, login_manager, db
from .entities import User, UnverifiedUser, PasswordResetRequest
from flask import request
import bcrypt
import flask_login
from lib.SendMail import send_mail_from_template
import secrets
import re
from datetime import date


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
        else:
            return {"status": "error", "message": "Das Passwort ist nicht korrekt"}, 403
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
