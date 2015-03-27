
require([
		"dojo/dom",
		"dojo/_base/config",
		"guestbookapp/view/GuestbookView",
		"guestbookapp/GuestbookStore",
		"dojo/domReady!"],
	function(dom, config, GuestbookWidget, GuestbookStore){
		var guestbook = dom.byId("Guestbook");
		var guestbook_name = config.guestbook_name;
		var currentUser = config.currentUser;
		var isAdmin = (config.isAdmin == 'True')? 1: 0 ;
		var guestbookStore = new GuestbookStore({'guestbook_name':guestbook_name });
		var data = {'guestbook_name': guestbook_name, 'guestbookStore': guestbookStore.guestbookStore , 'currentUser': currentUser, 'isAdmin': isAdmin};
		widget = new GuestbookWidget(data).placeAt(guestbook).startup();
	});