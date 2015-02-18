from google.appengine.ext import ndb
<<<<<<< HEAD
from django.core.urlresolvers import reverse
=======
from google.appengine.api import users
>>>>>>> origin/feature/django-refactoring

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.



class Guestbook(ndb.Model):
	'''Models an individual Guestbook entry.'''
	name = ndb.StringProperty(indexed=True)

	@staticmethod
	def get_guestbook(guestbook_name):
						try:
							return Guestbook.query(Guestbook.name == guestbook_name).get()
						except (RuntimeError, ValueError):
							return None
	
	@staticmethod
	def add_guestbook(guestbook_name):
			try:
				guestbook = Guestbook()
				guestbook.name = guestbook_name
				guestbook.put()
				return True
			except (RuntimeError, TypeError):
				return False

	@staticmethod
	def isExist(guestbook_name):
		if Guestbook.get_guestbook(guestbook_name) is None:
			return False
		else:
			return True

	@staticmethod
	def get_guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
		return ndb.Key('Guestbook', guestbook_name)

class Greeting(ndb.Model):
	'''Models an individual Guestbook entry.'''
	author = ndb.UserProperty()
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)
   
	@classmethod
	def get_latest(cls,guestbook_name,count):
					try:
						return cls.query(ancestor=Guestbook.get_guestbook_key(guestbook_name)).order(-cls.date).fetch(count)
					except ValueError:
						return None

<<<<<<< HEAD

=======
	@classmethod
	def put_from_dict(cls, dictionary):
				guestbook_name = dictionary.get("guestbook_name")
				if not guestbook_name:
					return DEFAULT_GUESTBOOK_NAME
				else:
					if Guestbook.isExist(guestbook_name) is False:
						Guestbook.add_guestbook(guestbook_name)
					greeting = cls(parent = Guestbook.get_guestbook_key(guestbook_name))
					if users.get_current_user():
							greeting.author = users.get_current_user()
					greeting.content = dictionary.get("greeting_message")
					greeting.put()
					return guestbook_name
>>>>>>> origin/feature/django-refactoring
