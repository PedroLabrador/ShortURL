#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

'''
Author: Pedro Labrador @SrPedro at Telegram
'''

import config, database, validators, random
from flask import Flask, request, redirect

app = Flask(__name__)

class Shortener():
	def __init__(self):
		database.create_tables(app)


	@app.route("/", methods=['GET'])
	def home():
		return """
				<div>
					<a href="/shorten">Shorten URLs here!</a>
				</div>
			"""


	@app.route("/shorten", methods=["GET"])
	def shorten_get():
		return	"""
				<div>
					<form action="/shorten" method="POST">
						<input type="text" name="url" />
						<input type="submit" value="Send" />
					</form>
				</div>
			"""


	@app.route("/shorten", methods=["POST"])
	def shorten_post():
		url = request.form['url']
		trimmed_url = url
		generated_url = ''

		def keep_alpha_string(string):
			return "".join(letter for letter in string if letter.isalpha())

		def lower_upper_string(string):
			return "".join(letter.lower() if not random.choice([0, 1]) else letter.upper() for letter in string)

		def random_string(string, stringLength=5):
			return "".join(random.choice(string) for i in range(stringLength))

		if validators.url(url):
			trimmed_url = keep_alpha_string(url)
			trimmed_url = lower_upper_string(trimmed_url)
			while True:
				generated_url = random_string(trimmed_url)
				if database.check_url(app, generated_url) is 0:
					database.insert_url(app, url, generated_url)
					break

		path = request.url_root + "redirect/" + generated_url
		return """
			<div>
				Your shortened URL is <a href="%s">%s</a>
			</div>
		""" % (path, path)


	@app.route("/redirect/<string:generated_url>", methods=['GET'])
	def redirect(generated_url):
		if database.check_url(app, generated_url) > 0:
			url = database.get_url(app, generated_url)
			return redirect(url)
		else:
			return "URL not found"


shortener = Shortener()

if __name__ == "__main__":
	app.run(debug=config.DEBUG)
