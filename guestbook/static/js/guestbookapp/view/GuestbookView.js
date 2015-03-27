define([
		"dojo/_base/declare",
		"dojo/_base/lang",
		"dojo/dom",
		"dojo/dom-construct",
		"dojo/_base/array",
		"dojo/on",
		"dojo/text!./templates/GuestbookWidget.html",
		"dijit/layout/ContentPane",
		"dijit/form/ValidationTextBox",
		"dijit/form/Button",
		"dijit/form/Form",
		"dijit/Dialog",
		"dijit/form/TextBox",
		"guestbookapp/view/GreetingView",
		"guestbookapp/view/_ViewBaseMixin",
		"dojo/domReady!"
	   ], function(declare, lang, dom, domConstruct, array, on, template, contentpane,  validtextbox, button, form,
				     dialog, textbox, GreetingView, _ViewBaseMixin){
	return declare('guestbookWidget', [_ViewBaseMixin], {
		//	set our template
		dict: null,
		templateString: template,
		guestbookStore: null,
		//	some properties
		guestbook_name : 'temp_guestbook',
		isAdmin: 0,
		currentUser: null,
		greetings: [],

		constructor: function (params) {
            this.guestbook_name = params.guestbook_name;
			this.guestbookStore = params.guestbookStore;
			this.isAdmin = params.isAdmin;
			this.currentUser = params.currentUser;
        },

		postCreate: function(){
			this.inherited(arguments);
			this.own( on(this.get_list, "click", lang.hitch(this, "getList")),
					  on(this.sign, "click", lang.hitch(this, "signGreeting")),
					  on(this.delete_all, "click", lang.hitch(this, "deleteAll")),
					  on(this.ok_detail, "click", lang.hitch(this, "hidePopup"))
					);
		},

		getList: function() {
			var guestbook_name = dijit.byId('guestbook').get('value');
			this.guestbookStore.query().then(lang.hitch(this, function(result){
				var greetings = dom.byId('greetingContainer');
				var list = result['object_list']['greetings'];
				if (list.length > 0){
					array.forEach(list, lang.hitch(this, function(greeting, i){

						data = {
							guestbookWidget: this,
							guestbook_name: guestbook_name,
							isAdmin: this.isAdmin,
							currentUser: this.currentUser,
							id: greeting.id,
							author: greeting.author,
							content: greeting.content
						}
						var widget = new GreetingView(data);
						widget.placeAt(greetings).startup();
						this.greetings.push(widget);
						console.log(this.greetings);
					}));
					if(this.isAdmin) {
						dojo.style(this.delete_div, 'display', '');
					}
				}
			}));

		},

		hidePopup: function(){
			this.detail_dialog.hide();
		},


		signGreeting: function() {
			postData = {
					guestbook_name: dijit.byId('guestbook').get('value'),
					greeting_message: dijit.byId('content_dialog').get('value')
				}
			this.guestbookStore.add(postData);
			//alert(123);
		},

		deleteAll: function() {
			dojo.query('.greetingWidget').forEach(function(node){
				dijit.byNode(node).deleteWidget(); // destroy ID
				domConstruct.destroy(node); // destroy innerHTML
			});
		}

	});
});