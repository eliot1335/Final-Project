from flask import Flask, render_template, redirect, jsonify, request
from flask_pymongo import PyMongo
import pymongo
import sys
import json
from bson import json_util
from bson.json_util import dumps
import urllib.parse
import joblib
from keras.models import load_model
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from tensorflow.keras.utils import to_categorical


app = Flask(__name__)

# Load the "sean" models
sean_model_lr_le = joblib.load("Saved_Models/sean_logistic_regression_le.sav")
sean_model_rf_le = joblib.load("Saved_Models/sean_random_forest_le.sav")
sean_model_knn_le = joblib.load("Saved_Models/sean_keras_neural_net_le.sav")

sean_model_logistic_regression = joblib.load("Saved_Models/sean_Logistic_Regression.sav")
sean_model_random_forest = joblib.load("Saved_Models/sean_Random_Forest.sav")
sean_model_keras = load_model("Saved_Models/sean_Neural_Net_1.h5")


# Utility Function for data cleaning pipeline
def text_pipeline(text):
    # split into words
    tokens = word_tokenize(text)
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    # join the words and return them to be loaded into the dataframe
    return " ".join(words)


###############################################################################################
# Base route on bring up
@app.route("/")
def index():
    return render_template("home.html")

# profitability route
@app.route("/profit", methods=['POST', 'GET'])
def profit():
    genDesc = "Fantasy: This is a sample movie description with lots of magic and monsters"
    if request.method == "POST":
        genDesc = request.form['gendesc']

    # get the spaces back from the content
    genDesc = urllib.parse.unquote_plus(genDesc)

    # run the text pipeline first
    text_clean = text_pipeline(text)

    # encode the text
    lr_encoded_text = sean_model_lr_le.transform(text_clean)

    rf_encoded_text = sean_model_rf_le.transform(text_clean)

    nn_encoded_text_pre = sean_model_knn_le.transform(text_clean)
    nn_encoded_text = to_categorical(nn_encoded_text_pre)

    # do the predictions on all of the models
    predict_lr = sean_model_logistic_regression.predict(lr_encoded_text)
    predict_rf = sean_model_random_forest.predict(rf_encoded_text)
    predict_nn = sean_model_keras.predict(nn_encoded_text)

    # decode the predictions
    print(f"predict_lr:{predict_lr}")
    print(f"predict_rf:{predict_rf}")
    print(f"predict_nn:{predict_nn}")

    # create the rec dictionary with the prediction text
    rec = {"h2_string": text_clean}

    return render_template("profit.html", rec=rec)

###############################################################################################
# temp route
# @app.route("/temp")
# def scatter():
#     return render_template("temp.html")

# route for json object
# @app.route("/metadata/temp_json")
# def temp_json():

    # client = pymongo.MongoClient(conn)

    # jsonify template
    # connect to mongo db and collection
    # db = client.movies_db
    # movies = db.movie_table

    # fields = {"title": True, "budget": True, "revenue": True, "genres": True, "_id": False}

    # json_projects = movies.find({}, fields)

    # client.close()

    # json_projects = [project for project in json_projects]

    # print(type(json_projects))

    # return jsonify(json_projects)



if __name__ == "__main__":
    app.run(debug=True)