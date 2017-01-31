import logging
from google.appengine.ext import ndb


def set_second_offset(new_seconds):
	ndb_seconds_entity = ndb.Key('NdbSeconds', 'second-offset').get()
	if ndb_seconds_entity is None:
		new_ndb_seconds = NdbSeconds(seconds=new_seconds, id="second-offset")
		ndb_seconds_key = new_ndb_seconds.put()
		ndb_seconds_entity = ndb_seconds_key.get()
	ndb_seconds_entity.seconds = new_seconds
	ndb_seconds_entity.put()


def getSecondOffset():
	ndb_seconds_entity = ndb.Key('NdbSeconds', 'second-offset').get()
	if ndb_seconds_entity is None:
		logging.warning("No Entity, Creating one now...")
		set_second_offset(0.0)
		return 0.0
	seconds = ndb_seconds_entity.seconds
	return seconds


class NdbSeconds(ndb.Model):
	seconds = ndb.FloatProperty(default=0.0)