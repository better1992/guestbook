define([
	"dojo/_base/declare",
	"dojo/_base/lang",
	"dojo/store/JsonRest",
	"dojo/store/Memory",
	"dojo/cookie"
], function(declare, lang, JsonRest, Memory, _cookie) {
	return declare('GuestbookStore', [], {
		guestbookStore : null,
		target: "/guestbookapp/api/guestbook/{0}/greeting/",

		constructor: function (data) {
			this.guestbook_name = data.guestbook_name;
			var GuestbookMemoryStore = new Memory();
			this.target = lang.replace(this.target, [this.guestbook_name]);
			var GuestbookJsonRestStore = new JsonRest(
				{ target: this.target, headers: {"X-CSRFToken": _cookie('csrftoken')}}
			);
			this.guestbookStore = GuestbookJsonRestStore;
		},

		getGreetings: function() {
			return this.guestbookStore.query();
		},

		getGreeting: function(id) {
			return this.guestbookStore.get(id);
		},

		putGreeting: function(data) {
			this.guestbookStore.put(data);
		},

		deleteGreeting: function(id) {
			this.guestbookStore.remove(id);
		},

		signGreeting: function(data) {
			this.guestbookStore.add(data);
		}

	});
});
