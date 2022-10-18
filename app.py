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
        #A10 = int(request.form['A10'])
        A9 = int(request.form['A9'])
        A8 = int(request.form['A8'])
        #A7 = int(request.form['A7'])
        A6 = int(request.form['A6'])
        #A5 = int(request.form['A5'])
        A4 = int(request.form['A4'])
        A3 = int(request.form['A3'])
        A2 = int(request.form['A2'])
        #A1 = int(request.form['A1'])
        
        
        
        """
        Gender = int(request.form['Gender'])
        Age = int(request.form['Age'])
        Region = request.form['Region']
        family = int(request.form['Family member with ASD history'])
        
        
        
       
        
        
       
        
      
            
        #region
        if(Region == "Riyadh Province"):
            region = 1
        elif(Region == "Makkah Province"):
            region = 2
        elif(Region == "Madinah Province"):
            region = 3
        elif(Region == "Qassim Province"):
            region = 4
        elif(Region == "Eastern Province"):
            region = 5
        elif(Region == "Aseer Province"):
            region = 6 
        elif(Region == "Tabuk Province"):
            region = 7
        elif(Region == "Ha'il Province"):
            region = 8
        elif(Region == "Northern Borders Province"):
            region = 9
        elif(Region == "Jizan Province"):
            region = 10
        elif(Region == "Najran Province"):
            region = 11
        elif(Region == "Al Baha Province"):
            region = 12
        elif(Region == "Al Jawf Province"):
            region = 13
        else:
            print("Choose any of the regions above")
          
        
        #Family
        if(family == "Yes"):
            family = 1
        else:
            family = 0
        
        #stare
        if(stare == "Yes"):
            stare = 1
        else:
            stare = 0
        #look
        if(look == "Yes"):
            look = 1
        else:
            look = 0
        
        #eye_contact
        if(eye_contact == "Yes"):
            eye_contact = 1
        else:
            eye_contact= 0
        
        #point
        if(point == "Yes"):
            point = 1
        else:
            point = 0
        #pretend
        if(pretend == "Yes"):
            pretend = 1
        else:
            pretend = 0
        #follow
        if(follow == "Yes"):
            follow = 1
        else:
            follow = 0
        #comfort
        if(comfort == "Yes"):
            comfort = 1
        else:
            comfort = 0
        #first_word
        if(first_word== "Yes"):
            first_word = 1
        else:
            first_word = 0
        #gestures
        if(gestures == "Yes"):
            gestures = 1
        else:
            gestures = 0 
        """
       
        feature = scaler.fit_transform([[A9,A8,A6,A4,A3,A2,]])
        
        prediction = model.predict(feature)[0]
        # print(prediction) 
        # 
        if prediction==0:
            prediction = "YES" 
        else:
            prediction = "NO" 
    
    
        return render_template("index.html", prediction_text = "Chance of Autism spectrum is -->{}".format(prediction))
    else:
        return render_template("index.html")
    
if __name__ == "__main__":
    flask_app.run(debug=True)