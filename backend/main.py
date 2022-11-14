from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
db.init_app(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    login = user.query.filter_by(username=username, password=password).first()
    if login is not None:
        return { 'status': 'success' }
    else:
        return { 'status': 'fail' }

@app.route("/register", methods=["POST"])
def register():
    uname = request.form['username']
    email = request.form['email']
    passw = request.form['password']

    register = user(username = uname, email = email, password = passw)
    db.session.add(register)
    db.session.commit()

    return { 'status': 'success' }

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)