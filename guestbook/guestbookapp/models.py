from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext.db import Error
# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.


class AppConstants(object):
	@property
	def get_default_guestbook_name(self):
		return "default_guestbook"


class GuestBook(ndb.Model):
	"""Models an individual GuestBook entry."""
	name = ndb.StringProperty(indexed=True)

	@staticmethod
	def get_guestbook(guestbook_name):
		try:
			return GuestBook.query(GuestBook.name == guestbook_name).get()
		except (RuntimeError, ValueError):
			return None

	@staticmethod
	def add_guestbook(guestbook_name):
		try:
			guestbook = GuestBook()
			guestbook.name = guestbook_name
			guestbook.put()
			return True
		except (RuntimeError, TypeError):
			return False


def get_guestbook_key(guestbook_name=AppConstants().get_default_guestbook_name):
	return ndb.Key('GuestBook', guestbook_name)


def is_exist(guestbook_name):
	"""

	:rtype : Guestbook
	"""
	if GuestBook.get_guestbook(guestbook_name) is None:
		return False
	else:
		return True


class Greeting(ndb.Model):
	"""Models an individual GuestBook entry."""
	author = ndb.UserProperty()
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)
	update_by = ndb.UserProperty()
	update_date = ndb.DateTimeProperty(auto_now_add=False)

	@classmethod
	def get_latest(cls, guestbook_name, count, cursor):
		"""
 
		 :type cls: Greeting
		 """
		curs = Cursor(urlsafe=cursor)
		greets, next_curs, more = cls.query(ancestor=get_guestbook_key(guestbook_name)).order(
			-Greeting.date).fetch_page(
			count, start_cursor=curs)
		return greets, next_curs, more

	@classmethod
	def get_greeting(cls, guestbook_name, greeting_id):
		return cls.query(
			cls.key == ndb.Key("GuestBook", str(guestbook_name), "Greeting",
							   int(greeting_id))).get()

	@classmethod
	def put_from_dict(cls, dictionary):
		guestbook_name = dictionary.get("guestbook_name")
		if not guestbook_name:
			return False
		else:
			try:
				if is_exist(guestbook_name) is False:
					GuestBook.add_guestbook(guestbook_name)
				greeting = cls(parent=get_guestbook_key(guestbook_name))
				if users.get_current_user():
					greeting.author = users.get_current_user()
				greeting.content = dictionary.get("greeting_message")
				greeting.put()
				return greeting
			except Error:
				return None

	@classmethod
	def to_dict(cls):
		item = {
			'id': str(cls.key.id()),
			'author': str(cls.author),
			'content': cls.content,
			'date': str(cls.date),
			'updated_by': str(cls.update_by),
			'updated_date': str(cls.update_date),
		}
		return item

	@classmethod
	def edit_greeting(cls, dictionary):
		greeting_id = dictionary.get("greeting_id")
		greeting_content = dictionary.get("greeting_message")
		guestbook_name = dictionary.get("guestbook_name")
		try:
			greeting = cls.query(
				Greeting.key == ndb.Key("GuestBook", guestbook_name, "Greeting",
										int(greeting_id))).get()
			if greeting is None:
				greeting = cls(parent=get_guestbook_key(guestbook_name))
				if users.get_current_user():
					greeting.author = users.get_current_user()
			greeting.content = greeting_content
			greeting.put()
			return greeting
		except Error:
			return None

	@classmethod
	def delete_greeting(cls, dictionary):
		greeting_id = dictionary.get("id")
		guestbook_name = dictionary.get("guestbook_name")
		try:
			greeting = cls.query(ndb.Key("GuestBook", guestbook_name, "Greeting",
										 int(greeting_id)) == Greeting.key).get()
			if greeting is None:
				return False
			else:
				greeting.key.delete()
				return True
		except Error:
			return False
