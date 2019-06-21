from flask import Flask, render_template, jsonify, redirect
import pymongo
import json
from bson import json_util
from flask_pymongo import PyMongo
import os
import scrape_jobs

conn = os.environ.get('MONGODB_URI')
if not conn:
   	conn = "mongodb://localhost:27017"

app = Flask(__name__)
app.config['MONGODB_URI'] = conn

# conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.job_search_db
collection = db.search_results

#mongo = PyMongo(app, uri="mongodb://localhost:27017/job_search_db")

@app.route('/')
def index():
	jobs = list(collection.find())
	return render_template('index.html', jobs=jobs)

@app.route('/api')
def json():
	data = []
	for x in collection.find():
		x.pop('_id')
		data.append(x)
	return jsonify(data)

@app.route('/<job_input>')
def scraper(job_input):
	jobs_data = scrape_jobs.scrapeIndeed(job_input)

	for i in jobs_data:
		i.pop('_id')

	jobs = list(collection.find())
	return redirect("/", code=302)

if __name__ == '__main__':
	app.run(debug=True)