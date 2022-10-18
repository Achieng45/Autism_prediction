import numpy as np
import joblib
import pickle 
from flask import Flask, request, jsonify, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, BooleanField
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import InputRequired, Email, Length
#from flask_login import LoginUser, UserMixin, login_user, login_required, logout_user
from sklearn.preprocessing import StandardScaler
scaler =StandardScaler()
model = pickle.load(open("model.pkl", "rb"))

# Create flask app
app=flask_app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
#login_user = LoginUser()
#login_user.init_app(app)
#login_user.login_view = 'login'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    
"""@login_user.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

@app.route('/')
def index1():
    return render_template("index1.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return render_template("login.html", form=form)
    return render_template("login.html", form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")
    return render_template('signup.html', form=form)  

@app.route("/dashboard")
#@login_required
def dashboard():
    return render_template("dashboard.html")
"""
@flask_app.route("/analysis")
def analysis():
    return render_template("index.html")

@flask_app.route("/", methods = ["GET","POST"])
def home():
    if request.method == "POST":
        
        A9 = int(request.form['A9'])
        A8 = int(request.form['A8'])
        
        A6 = int(request.form['A6'])
        
        A4 = int(request.form['A4'])
        A3 = int(request.form['A3'])
        A2 = int(request.form['A2'])
        
       
        Gender = int(request.form['Gender'])
        
        Region = int(request.form['Reqion'])
        family = int(request.form['Family member with ASD history'])
       
        feature = scaler.fit_transform([[A10,A9,A8,A7,A6,A5,A4,A3,A2,A1,Region,family,Age,Gender]])
        
        prediction = model.predict(feature)[0]
        # print(prediction) 
        # 
        if prediction==0:
            prediction = "NO" 
        else:
            prediction = "YES" 
    
    
        return render_template("index.html", prediction_text = "Chance of Autism Prediction is -->{}".format(prediction))
    else:
        return render_template("index.html")
    
if __name__ == "__main__":
    flask_app.run(debug=True)