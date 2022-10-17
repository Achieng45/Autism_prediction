import numpy as np

from flask import Flask, request, jsonify, render_template
import pickle
from sklearn.preprocessing import StandardScaler
scaler =StandardScaler()
model = pickle.load(open("model.pkl", "rb"))

# Create flask app
flask_app = Flask(__name__)
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