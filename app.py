from flask import Flask, render_template, redirect, jsonify, request
from flask_pymongo import PyMongo
import pymongo
import sys
import json
from bson import json_util
from bson.json_util import dumps


app = Flask(__name__)
# setup mongo connection
conn = "mongodb://localhost:27017"


###############################################################################################
# Base route on bring up
@app.route("/")
def index():
    return render_template("home.html")

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