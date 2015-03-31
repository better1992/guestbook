
require([
		"dojo/dom",
		"guestbookapp/view/GuestbookView",
		"dojo/domReady!"],
	function(dom, GuestbookWidget){
		var guestbook = dom.byId("Guestbook");
		widget = new GuestbookWidget()
		widget.placeAt(guestbook);
		widget.startup();
	});