# -*- coding: utf-8 -*-
from mongoengine import *

from flask.ext.mongoengine.wtf import model_form
from datetime import datetime

class Comment(EmbeddedDocument):
	name = StringField()
	comment = StringField()
	timestamp = DateTimeField(default=datetime.now())

class Dreamology(Document):

	title = StringField(max_length=120, required=True)
	slug = StringField()
	dream = StringField()
	postedby = StringField(max_length=120, required=True, verbose_name="Your name")
	
	categories = ListField( StringField() )
	tags = StringField(max_length=120, required=False)

	# Comments is a list of Document type 'Comments' defined above
	comments = ListField( EmbeddedDocumentField(Comment) )

	# Timestamp will record the date and time dream was created.
	timestamp = DateTimeField(default=datetime.now())

DreamologyForm = model_form(Dreamology)

	

