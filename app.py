# -----------------------------
# --------- Libraries ---------
# -----------------------------

# -*- coding: utf-8 -*-
import os, datetime, re
from unidecode import unidecode

from flask import jsonify

from flask import Flask, request, render_template, redirect, abort

# import all of mongoengine
# from mongoengine import *
from flask.ext.mongoengine import mongoengine

# import data models
import models

app = Flask(__name__)   # create our flask app



# ---------------------------------------
# --------- Database Connection ---------
# ---------------------------------------

# MongoDB connection to MongoLab's database
mongoengine.connect('mydata', host=os.environ.get('MONGOLAB_URI'))
app.logger.debug("Connecting to MongoLabs")



# -----------------------------
# ----------- Lists -----------
# -----------------------------

# Create the lists that match the name of the ListField in the models.py
categories = ['fairy tales', 'fantasy', 'mystery', 'real stories', 'romance', 'sci-fi', 'suspense']



# ---------------------------
# --------- Routes ----------
# ---------------------------


# this is our main page
@app.route("/", methods=['GET','POST'])
def index():

	all_dreams = models.Dreamology.objects.order_by('-timestamp')

	return render_template("main.html", dreams=all_dreams)



# this is the Page to Submit NEW Dreams
@app.route("/submit", methods=['GET','POST'])
def submit():

	app.logger.debug(request.form.getlist('categories'))

	# get Dreamology form from models.py
	dreamology_form = models.DreamologyForm(request.form)
	
	if request.method == "POST" and dreamology_form.validate():
	
		now = datetime.datetime.now()

	# get form data - create new dream post
		dream_post = models.Dreamology()
		
		dream_post.title = request.form.get('title')
		dream_post.dream = request.form.get('dream','')
		dream_post.postedby = request.form.get('postedby')
		dream_post.tags = request.form.get('tags')
		dream_post.slug = slugify(dream_post.title + "-" + now.strftime("%f"))
	
		dream_post.save()

		return redirect('/dream/%s' % dream_post.slug)

	else:

		if request.form.getlist('categories'):
			for c in request.form.getlist('categories'):
				dreamology_form.categories.append_entry(c)

		templateData = {
			'dreams' : models.Dreamology.objects(),
			'categories' : categories,
			'form' : dreamology_form
		}

		return render_template("submit.html", **templateData)


# Dreams Page
@app.route("/dream/<dream_post_slug>")
def dream_display(dream_post_slug):

	# get dream by dream_post_slug
	try:
		dream_post = models.Dreamology.objects.get(slug=dream_post_slug)
	except:
		abort(404)

	tag_str = ", ".join(dream_post.tags)

	# prepare template data
	templateData = {
		'dream_post' : dream_post,
		'tags' : tag_str
	}

	# render and return the template
	return render_template('idea_entry.html', **templateData)


# Comments Page
@app.route("/dream/<dream_id>/comment", methods=['POST'])
def dream_comment(dream_id):

	name = request.form.get('name')
	comment = request.form.get('comment')

	if name == '' or comment == '':
		# no name or comment, return to page
		return redirect(request.referrer)

	#get the dreams by id
	try:
		dream_post = models.Dreamology.objects.get(id=dream_id)			

	except:
		# error, return to where you came from
		return redirect(request.referrer)


	# create comment
	commentary = models.Comment()
	commentary.name = request.form.get('name')
	commentary.comment = request.form.get('comment')
	
	# append comment to dream
	dream_post.comments.append(commentary)

	# save it
	dream_post.save()

	return redirect('/dream/%s' % dream_post.slug)



# ----------------------------
# --------- Helpers ----------
# ----------------------------

# Handle Errors
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# Slugify the title to create URLS
# via http://flask.pocoo.org/snippets/5/
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
def slugify(text, delim=u'-'):
	"""Generates an ASCII-only slug."""
	result = []
	for word in _punct_re.split(text.lower()):
		result.extend(unidecode(word).split())
	return unicode(delim.join(result))



# ------------------------------
# --------- Server On ----------
# ------------------------------

# start the webserver
if __name__ == "__main__":
	app.debug = True
	
	port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
	app.run(host='0.0.0.0', port=port)



	