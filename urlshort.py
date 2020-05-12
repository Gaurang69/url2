#!/usr/bin/python3
# -*- coding: utf-8 -*-
#vim: set tabstop=2
from flask import Flask, g, request, render_template, redirect
import sqlite3
import random
import string
import math
import time
from flask_limiter import Limiter
from contextlib import closing
from urllib.parse import urlparse

app = Flask(__name__)
app.config.from_object("settings")
limiter = Limiter(app, global_limits=["2 per minute", "100 per day"])

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, "db", None)
	if db is not None:
		db.close()

@app.route("/")
@limiter.exempt
def root():
	return render_template("create.html")

@app.route("/<pasteID>")
@limiter.exempt
def paste(pasteID):
	target = query_db("SELECT target FROM pastes WHERE paste_url = ?", [pasteID], one=True)
	if target is None:
		return redirect("/", 301)
	else:
		url = urlparse(target["target"]).geturl()
		# Here is the right place to implement different redirection methods
		return redirect(target, 301)

@app.route("/new")
@limiter.exempt
def new_short():
	target_url = request.args.get("target", "")
	target_url = urlparse(target_url)
	if target_url.path is "" and target_url.netloc is "":
		return "invalid request!"
	if url.scheme is "":
		target_url = "http://" + target_url.geturl()
	else:
		target_url = target_url.geturl()
	paste_id = add_redirect(target_url, 1)
	return render_template("short_completed.html", paste_id=paste_id, server_url=request.host + "/")

def add_redirect(target_url, method_id):
	paste_id = gen_new_id(5)
	ip = request.remote_addr
	timestamp = int(time.time())
	db = getattr(g, "db", None)
	if db is not None:
		query = "INSERT INTO pastes (paste_url, target, method_id, ip, timestamp) VALUES (:paste_url, :target, :method_id, :ip, :timestamp);"
		args = {"paste_url" : paste_id, "target" : target_url, "method_id" : "1", "ip" : ip, "timestamp" : timestamp}
		db.cursor().execute(query, args)
		db.commit()
		db.close()
	return paste_id

def gen_new_id(length):
	while True:	
		new_id = "".join([random.choice(string.ascii_letters + string.digits) for n in range(length)])
		if query_db("SELECT * FROM pastes WHERE paste_url = ?", [new_id], one=True) is None:
			break	
	return new_id

def query_db(query, args=(), one=False):
	with closing(connect_db()) as db:
		db.row_factory = sqlite3.Row
		cur = db.cursor().execute(query, args)
		rv = cur.fetchall()
		cur.close()
		return (rv[0] if rv else None) if one else rv

def init_db():
	with closing(connect_db()) as db:
		db.cursor().executescript(app.config["DEFAULT_SCHEMA"])
		db.commit()

def connect_db():
	return sqlite3.connect(app.config["DATABASE"])

if __name__ == "__main__":
	app.run(debug=app.config["DEBUG"])
