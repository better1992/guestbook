define([
	"dojo/_base/declare",
	"dojo/_base/lang",
	"dojo/store/JsonRest",
	"dojo/cookie"
], function(declare, lang, JsonRest, cookie) {
	return declare('GuestbookStore', [], {
		guestbookStore : null,
		target: "/guestbookapp/api/guestbook/{0}/greeting/",

		constructor: function (data) {
			this.guestbook_name = data.guestbook_name;
			target = lang.replace(this.target, [this.guestbook_name]);
			var GuestbookJsonRestStore = new JsonRest(
				{ target: target, headers: {"X-CSRFToken": cookie('csrftoken')}}
			);
			this.guestbookStore = GuestbookJsonRestStore;
		},

		getGreetings: function(data) {
			this.guestbook_name = data.guestbook_name;
			this.guestbookStore.target = lang.replace(this.target, [this.guestbook_name]);
			return this.guestbookStore.query();
		},

		getGreeting: function(id) {
			return this.guestbookStore.get(id);
		},

		putGreeting: function(data) {
			return this.guestbookStore.put(data);
		},

		deleteGreeting: function(id) {
			this.guestbookStore.remove(id);
		},

		signGreeting: function(data) {
			return this.guestbookStore.add(data);
		}

	});
});
