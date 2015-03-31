import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext.db import Error
# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.


class AppConstants(object):
	@property
	def get_default_guestbookName(self):
		return "demo"


class GuestBook(ndb.Model):
	"""Models an individual GuestBook entry."""
	name = ndb.StringProperty(indexed=True)

	@staticmethod
	def get_guestbook(guestbookName):
		try:
			return GuestBook.query(GuestBook.name == guestbookName).get()
		except (RuntimeError, ValueError):
			return None

	@staticmethod
	def add_guestbook(guestbookName):
		try:
			guestbook = GuestBook()
			guestbook.name = guestbookName
			guestbook.put()
			return True
		except (RuntimeError, TypeError):
			return False


def get_guestbook_key(guestbookName=AppConstants().get_default_guestbookName):
	return ndb.Key('GuestBook', guestbookName)


def is_exist(guestbookName):
	"""

	:rtype : Guestbook
	"""
	if GuestBook.get_guestbook(guestbookName) is None:
		return False
	else:
		return True


class Greeting(ndb.Model):
	"""Models an individual GuestBook entry."""
	author = ndb.UserProperty()
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)
	update_by = ndb.StringProperty()
	update_date = ndb.DateTimeProperty(auto_now_add=False)

	@classmethod
	def get_latest(cls, guestbookName, count, cursor):
		"""
 
		 :type cls: Greeting
		 """
		curs = Cursor(urlsafe=cursor)
		greets, next_curs, more = cls.query(ancestor=get_guestbook_key(guestbookName)).order(
			-Greeting.date).fetch_page(
			count, start_cursor=curs)
		return greets, next_curs, more

	@classmethod
	def get_greeting(cls, guestbookName, greeting_id):
		return cls.query(
			cls.key == ndb.Key("GuestBook", str(guestbookName), "Greeting",
							   int(greeting_id))).get()

	@classmethod
	def put_from_dict(cls, dictionary):
		guestbookName = dictionary.get("guestbookName")
		if not guestbookName:
			return False
		else:
			try:
				if is_exist(guestbookName) is False:
					GuestBook.add_guestbook(guestbookName)
				greeting = cls(parent=get_guestbook_key(guestbookName))
				if users.get_current_user():
					greeting.author = users.get_current_user()
				greeting.content = dictionary.get("greeting_message")
				greeting.put()
				return greeting
			except Error:
				return None

	def to_dict(self):
		if self.author is None:
			author = 'Anonymous'
		else:
			author = str(self.author)
		item = {
			'id': self.key.id(),
			'author': author,
			'content': str(self.content),
			'dateCreated': str(self.date),
			'updatedBy': str(self.update_by),
			'updatedDate': str(self.update_date),
		}
		return item

	@classmethod
	def edit_greeting(cls, dictionary):
		try:
			greeting_id = dictionary["id"]
			greeting_content = dictionary["content"]
			guestbookName = dictionary["guestbookName"]
			updated_by = dictionary['updated_by']
			greeting = cls.query(
				Greeting.key == ndb.Key("GuestBook", guestbookName, "Greeting",
										int(greeting_id))).get()
			greeting.update_by = updated_by
			greeting.update_date = datetime.datetime.now()
			greeting.content = greeting_content
			greeting.put()
			return greeting
		except Error, ValueError:
			return None

	@classmethod
	def delete_greeting(cls, dictionary):
		greeting_id = dictionary.get("id")
		guestbookName = dictionary.get("guestbookName")
		try:
			greeting = cls.query(ndb.Key("GuestBook", guestbookName, "Greeting",
										 int(greeting_id)) == Greeting.key).get()
			if greeting is None:
				return False
			else:
				greeting.key.delete()
				return True
		except Error:
			return False
