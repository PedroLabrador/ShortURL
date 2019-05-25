#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

'''
Author: Pedro Labrador @SrPedro at Telegram
'''

import config, sqlite3
from flask import g

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(config.DATABASE)
	return db


def create_tables(app):
	with app.app_context():
		db = get_db()
		cursor = db.cursor()
		cursor.execute(	"""
			CREATE TABLE IF NOT EXISTS shorten (
				id 				INTEGER PRIMARY KEY AUTOINCREMENT,
				url 			VARCHAR,
				shorturl 	VARCHAR,
				date			TIMESTAMP)
		""")
		db.commit()


def check_url(app, url):
	with app.app_context():
		db = get_db()
		cursor = db.cursor()
		cursor.execute(	"""
			SELECT COUNT(*) FROM shorten WHERE shorturl = '%s'
		""" % (url))
		return cursor.fetchone()[0]


def insert_url(app, url, generated_url):
	with app.app_context():
		db = get_db()
		cursor = db.cursor()
		cursor.execute(	"""
			INSERT INTO shorten (url, shorturl, date) VALUES ('%s', '%s', DateTime('now'))
		""" % (url, generated_url))
		db.commit()


def get_url(app, generated_url):
	with app.app_context():
		db = get_db()
		cursor = db.cursor()
		cursor.execute( """
			SELECT url FROM shorten WHERE shorturl = '%s'
		""" % (generated_url))
		return cursor.fetchone()[0]
