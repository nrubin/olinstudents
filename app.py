import os, random, string, requests, json, re, time
import hashlib, requests, json, time, os, re, urllib
from urlparse import urlparse

from flask import Flask, session, request, redirect, url_for, render_template, jsonify, Response
app = Flask(__name__, static_url_path='')
Flask.secret_key = os.environ.get('FLASK_SESSION_KEY', os.environ.get('SECRET_KEY', 'test-key-please-ignore'))

PORT = int(os.environ.get('PORT', 5000))
if 'PORT' in os.environ:
	HOSTNAME = 'directory.olinapps.com'
	HOST = 'directory.olinapps.com'
else:
	HOSTNAME = 'localhost'
	HOST = 'localhost:5000'

# Mongo
# -----------

from pymongo import Connection, ASCENDING, DESCENDING
from bson.code import Code
from bson.objectid import ObjectId

if os.environ.has_key('MONGOLAB_URI'):
	mongodb_uri = os.environ['MONGOLAB_URI']
	db_name = 'heroku_app9884622'
else:
	mongodb_uri = "mongodb://localhost:27017/"
	db_name = 'olinapps-directory'

connection = Connection(mongodb_uri)
db = connection[db_name]

USER_KEYS = ['name', 'nickname', 'room', 'year', 'phone', 'mail', 'website', 'show_website',
	'twitter', 'facebook', 'tumblr', 'skype', 'pinterest', 'lastfm', 'google',
	'preferredemail'];

def db_user_json(user):
	json = dict(id=str(user['_id']), email=user['email']);
	for key in USER_KEYS:
		json[key] = user.get(key, '')
	json['domain'] = user['email'].split('@', 1)[1]
	return json

@app.route('/')
def website():
	"""
	This method needs to return a dictionary of years:users with websites in those years
	"""
	users = db.users.find({'show_website':'on'})
	year_users = {}
	for userd in users:
		user = db_user_json(userd)
		year = user['year']
		if year_users.has_key(year):
			year_users[year].append(user)
		else:
			year_users[year] = [user]
	print year_users
	return render_template('websites.html',
		year_users = year_users)


# Launch
# ------

app.debug = True

if __name__ == '__main__':
	# Bind to PORT if defined, otherwise default to 5000.
	app.debug = True
	app.run(host=HOSTNAME, port=PORT)
