define([
		"dojo/_base/declare",
		"dojo/_base/lang",
		"dojo/store/JsonRest",
		"dojo/store/Cache",
		"dojo/store/Memory",
		"dojo/store/Observable",
		"dojo/cookie"
   ], function(declare, lang, JsonRest, Cache, Memory, Observable, _cookie) {
	return declare([], {
		guestbookStore : null,
		target: "/guestbookapp/api/guestbook/{0}/greeting/",

		constructor: function (data) {
            this.guestbook_name = data.guestbook_name;
			var GuestbookMemoryStore = new Observable(new Memory());
			this.target = lang.replace(this.target, [this.guestbook_name]);
			var GuestbookJsonRestStore = new JsonRest(
				{ target: this.target, headers: {"X-CSRFToken": _cookie('csrftoken')}}
			);
			this.guestbookStore = GuestbookJsonRestStore;
        }
	});
});
