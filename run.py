import pickle
from flask import Flask, request, render_template
from flask_cors import cross_origin
import joblib

app = Flask(__name__)

modelfinal = joblib.load(open("C:/Users/navee/OneDrive/Desktop/VINAUDIT/lgr", "rb"))
mapping =joblib.load(open("C:/Users/navee/OneDrive/Desktop/VINAUDIT/mppi", "rb"))
mapping1 =joblib.load(open("C:/Users/navee/OneDrive/Desktop/VINAUDIT/mppi1", "rb"))
mapping2 =joblib.load(open("C:/Users/navee/OneDrive/Desktop/VINAUDIT/mppi2", "rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")

@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        year = int(request.form["year"])
        #print(request.form["model"].upper() in mapping)
        if ((request.form["make"].upper() in mapping) and  (request.form["model"] in mapping1) and (request.form["dealer_state"].upper() in mapping2)):         
            make = int(mapping[request.form["make"].upper()])
            model=int(mapping1[request.form["model"]])
            dealer_state = int(mapping2[request.form["dealer_state"].upper()])
            listing_mileage = float(request.form["listing_mileage"])

            # Make a prediction using the loaded model
            prediction = modelfinal.predict([[year, make, model, listing_mileage, dealer_state]]) 
            output = round(prediction[0], 2)
        else:
            output = "Required data not found"                             
            
        return render_template('home.html', prediction_text=output)

    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
