# -*- coding: utf-8 -*-
from flask.ext.mongoengine.wtf import model_form
from wtforms.fields import * # for our custom signup form
from flask.ext.mongoengine.wtf.orm import validators
from flask.ext.mongoengine import *
from datetime import datetime

class Comment(mongoengine.EmbeddedDocument):
	name = mongoengine.StringField()
	comment = mongoengine.StringField()
	timestamp = mongoengine.DateTimeField(default=datetime.now())

class Dreamology(mongoengine.Document):

	title = mongoengine.StringField(max_length=120, required=True)
	slug = mongoengine.StringField()
	dream = mongoengine.StringField()
	postedby = mongoengine.StringField(max_length=120, required=True, verbose_name="Your name")
	
	categories = mongoengine.ListField( StringField() )
	tags = mongoengine.ListField( mongoengine.StringField())

	# Comments is a list of Document type 'Comments' defined above
	comments = mongoengine.ListField( mongoengine.EmbeddedDocumentField(Comment) )

	# Timestamp will record the date and time dream was created.
	timestamp = mongoengine.DateTimeField(default=datetime.now())

dreamm_form = model_form(Dreamology)

	

