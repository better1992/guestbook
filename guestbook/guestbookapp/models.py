	"""Models an individual GuestBook entry."""
+	author = ndb.UserProperty()
+	content = ndb.StringProperty(indexed=False)
+	date = ndb.DateTimeProperty(auto_now_add=True)
+	update_by = ndb.UserProperty()
+	update_date = ndb.DateTimeProperty(auto_now_add=False)
+
+	@classmethod
+	def get_latest(cls, guestbook_name, count, cursor):
+		"""
+
+		:type cls: Greeting
+		"""
+		curs = Cursor(urlsafe=cursor)
+		greets, next_curs, more = cls.query(ancestor=get_guestbook_key(guestbook_name)).order(-Greeting.date).fetch_page(
+			count, start_cursor=curs)
+		return greets, next_curs, more
+
+	@classmethod
+	def get_greeting(cls, guestbook_name, greeting_id):
+		return cls.query(
+			ndb.Key("GuestBook", str(guestbook_name), "Greeting",
+					int(greeting_id)) == cls.key).get()
+
+	@classmethod
+	def put_from_dict(cls, dictionary):
+		guestbook_name = dictionary.get("guestbook_name")
+		if not guestbook_name:
+			return False
+		else:
+			try:
+				if is_exist(guestbook_name) is False:
+					GuestBook.add_guestbook(guestbook_name)
+				greeting = cls(parent=get_guestbook_key(guestbook_name))
+				if users.get_current_user():
+					greeting.author = users.get_current_user()
+				greeting.content = dictionary.get("greeting_message")
+				greeting.put()
+				return greeting
+			except Error:
+				return None
+
+	@classmethod
+	def to_dict(cls):
+		item = {
+			'id': str(cls.key.id()),
+			'author': str(cls.author),
+			'content': cls.content,
+			'date': str(cls.date),
+			'updated_by': str(cls.update_by),
+			'updated_date': str(cls.update_date),
+			}
+		return item
+
+	@classmethod
+	def edit_greeting(cls, dictionary):
+		greeting_id = dictionary.get("greeting_id")
+		greeting_content = dictionary.get("greeting_message")
+		guestbook_name = dictionary.get("guestbook_name")
+		try:
+			greeting = cls.query(
+				Greeting.key == ndb.Key("GuestBook", guestbook_name, "Greeting",
+										int(greeting_id))).get()
+			if greeting is None:
+				greeting = cls(parent=get_guestbook_key(guestbook_name))
+				if users.get_current_user():
+					greeting.author = users.get_current_user()
+			greeting.content = greeting_content
+			greeting.put()
+			return greeting
+		except Error:
+			return None
+
+	@classmethod
+	def delete_greeting(cls, dictionary):
+		greeting_id = dictionary.get("id")
+		guestbook_name = dictionary.get("guestbook_name")
+		try:
+			greeting = cls.query(Greeting.key == ndb.Key("GuestBook", guestbook_name, "Greeting",
+														 int(greeting_id))).get()
+			if greeting is None:
+				return False
+			else:
+				greeting.key.delete()
+				return True
+		except Error:
+			return False
