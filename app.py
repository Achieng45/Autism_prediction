
from django.shortcuts import render
import numpy as np
import joblib
import pickle 
from flask import Flask, flash, request, jsonify, render_template, redirect, url_for, request,session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL, MySQLdb
import flask_bcrypt
from flask_bcrypt import Bcrypt
import MySQLdb.cursors
from sklearn.preprocessing import StandardScaler
import re
import psycopg2 #pip install psycopg2 
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
scaler =StandardScaler()
model = pickle.load(open("model.pkl", 'rb'))


# Create flask app
app=flask_app = Flask(__name__)



app.config['SECRET_KEY'] = 'secret'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'asd_prediction1'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
bootstrap = Bootstrap(app)
bcrypt=Bcrypt(app)

@app.route('/') 
def dashboard():
    return render_template("dashboard.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        
        First_name = request.form['First_name']
        Last_name = request.form['Last_name']
        Email = request.form['Email']
        Password = request.form['Password'].encode('utf-8')
        hash_password = bcrypt.generate_password_hash(Password)
    
        cur = mysql.connection.cursor()
         #check if account exixts
        cur.execute('SELECT * FROM user WHERE Email=%s',(Email,))
        account=cur.fetchone()
        if account:
            flash("Account already exists!")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',Email):
            flash('Invalid email Address')
        elif not Email or not Password or not First_name or  not Last_name:
            flash('Please fill out the form')
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO user(First_name,Last_name,Email,Password) VALUES (%s,%s,%s,%s)",(First_name,Last_name,Email,hash_password,))
            mysql.connection.commit()
            session['First_name'] = First_name
            session['Last_name']=Last_name
            session['Email']=Email
            cur.close()
           
            flash("Registerd successfully")
            return redirect(url_for("login"))
    
    return render_template('signup.html')
        
    
@app.route('/login', methods=["GET","POST"])
def login():
    msg=''
    
    if request.method == 'POST':
        Email = request.form['Email']
        Password = request.form['Password']
        cur = mysql.connection.cursor()
       
            
        result=cur.execute("SELECT * FROM user WHERE Email=%s",[Email])
        
        #curl.close()
        
        #users["Password"].encode('utf-8')
        if result>0:
            users = cur.fetchone()
            Password1=users['Password']
            if bcrypt.check_password_hash(Password1,Password):
                session['loggedin'] = True
                session['First_name'] = users['First_name']
                session['Last_name'] = users['Last_name']
                session['Email'] = users['Email']
                msg =" You have logged in successfully"
                return redirect(url_for("index"))
                cur.close()
            else:
                flash ( "Incorrect username or password")
        else:
            flash ( "User does not exist")
        
    return render_template("login.html")

@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('index.html',Email=session['Email'])
    return redirect(url_for('login'))

@app.route('/dashboard')
def logout():
    session.clear()
    return render_template("dashboard.html")

@app.route("/analysis")
def index():
    return render_template("index.html")


@app.route("/", methods = ["GET","POST"])
def index1():
    if request.method=="POST":
        A9 = int(request.form['A9'])
        A8 = int(request.form['A8'])
        A6 = int(request.form['A6'])
        A4 = int(request.form['A4'])
        A3 = int(request.form['A3'])
        A2 = int(request.form['A2'])
    
        feature = ([[A9,A8,A6,A4,A3,A2,]])
    
       
        prediction = model.predict(feature)
     
        if prediction==1:
            prediction = "The child has a high risk of Autism" 
        else:
            prediction = "The child has a low risk of Autism" 
    
    
        return render_template("asd_result.html", prediction_text = "{}".format(prediction))
    else:
        return render_template("index.html")

@app.route('/profile')
def profile(): 
    cur = mysql.connection.cursor()
  
    # Check if user is loggedin
    if 'loggedin' in session:
        cur.execute('SELECT * FROM users WHERE Email = %s', [session['Email']])
        account = cur.fetchone()
        # Show the profile page with account info
        return render_template('index.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.debug =True
    app.run(debug=True)