from flask import Flask, render_template, jsonify, redirect
import pymongo
import json
from bson import json_util
from flask_pymongo import PyMongo
import os
# import scrape_jobs

conn = os.environ.get('MONGODB_URI')
if not conn:
   	conn = "mongodb://localhost:27017/job_search_db"

app = Flask(__name__)

app.config["MONGO_URI"] = conn
mongo = PyMongo(app)


@app.route('/')
def index():
	jobs = mongo.db.search_results.find()
	return render_template('index.html', jobs=jobs)

@app.route('/api')
def json_api():
	data = []
	for x in mongo.db.search_results.find():
		x.pop('_id')
		data.append(x)
	return jsonify(data)

@app.route('/<job_input>')
def scraper(job_input):
	from scrape_jobs import scrapeIndeed
	jobs_data = scrapeIndeed(job_input)
	mongo.db.search_results.drop()
	jobs = mongo.db.search_results
	jobs.insert_many(jobs_data)
	return redirect("/", code=302)

if __name__ == '__main__':
	app.run(debug=True)