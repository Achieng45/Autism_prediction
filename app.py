from email import message
import numpy as np
import joblib
import pickle 
from flask import Flask, request, jsonify, render_template, redirect, url_for, request,session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
from sklearn.preprocessing import StandardScaler
scaler =StandardScaler()
model = pickle.load(open("model.pkl", "rb"))

# Create flask app
app=flask_app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'asd_prediction1'
mysql = MySQL(app)
bootstrap = Bootstrap(app)
    

@app.route('/')
def dashboard():
    return render_template("dashboard.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
   
    if request.method == "POST":
        Email = request.form['Email']
        Password = request.form['Password'].encode('utf-8')
        
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM user WHERE Email=%s AND Password=%s",(Email,Password,))
        user = cur.fetchone()
        cur.close()
        
        if user:
            #if bcrypt.hashpw(Password,user['Password'].encode('utf-8')) == user['Password'].encode('utf-8'):
                
            session['loggedin']= True
            #session['First_name']= user['First_name']
            #session['Last_name']=user['Last_name']
            session['Email'] = user['Email']
            message = 'Logged in successfully'
            return redirect(url_for("index"))
        else:
             return "Error wrong password or email"
               
        
    
    return render_template("index.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    else:
        User_id=['User_id']
        First_name = request.form['First_name']
        Last_name = request.form['Last_name']
        Email = request.form['Email']
        Password = request.form['Password'].encode('utf-8')
        hash_password = bcrypt.hashpw(Password,bcrypt.gensalt())
        
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("INSERT INTO user VALUES (%s,%s,%s,%s,%s)",(User_id,First_name,Last_name,Email,hash_password,))
        mysql.connection.commit()
        session['First_name'] = First_name
        session['Last_name']=Last_name
        session['Email']=Email
        return redirect(url_for("login"))
        
     
""""
@app.route("/dashboard")
#@login_required
def dashboard():
    return render_template("dashboard.html")
"""
@app.route('/logout')

def logout():
    session.clear()
    return redirect(url_for('index1'))
"""
@flask_app.route("/analysis")
def analysis():
    return render_template("index.html")
"""
@flask_app.route("/index", methods = ["GET","POST"])
def home():
    if request.method == "POST":
        #return render_template("index.html")
        
        A9 = int(request.form['A9'])
        A8 = int(request.form['A8'])
        A6 = int(request.form['A6'])
        A4 = int(request.form['A4'])
        A3 = int(request.form['A3'])
        A2 = int(request.form['A2'])
      
        feature = scaler.fit_transform([[A9,A8,A6,A4,A3,A2,]])
        
        prediction = model.predict(feature)[0]
        
        if prediction==0:
            prediction = "YES" 
        else:
            prediction = "NO" 
    
    
        return render_template("index.html", prediction_text = "Chance of Autism spectrum is -->{}".format(prediction))
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.debug =True
    flask_app.run(debug=True)