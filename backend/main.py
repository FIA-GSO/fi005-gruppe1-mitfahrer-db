from flask import render_template, send_from_directory
from server import app, db
from routes import rides, user


@app.route("/images/<path:path>")
def send_report(path):
    return send_from_directory("images", path)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        print("Creating Database...")
        db.create_all()
    app.run(debug=True)
