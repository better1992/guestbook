define([
	"dojo/_base/declare",
	"dojo/_base/lang",
	"dojo/_base/array",
	"dojo/_base/config",
	"dojo/dom",
	"dojo/dom-construct",
	"dojo/on",
	"dojo/text!./templates/GuestbookView.html",
	"dijit/layout/ContentPane",
	"dijit/form/ValidationTextBox",
	"dijit/form/Button",
	"dijit/form/Form",
	"dijit/Dialog",
	"dijit/form/TextBox",
	"guestbookapp/GuestbookStore",
	"guestbookapp/view/GreetingView",
	"guestbookapp/view/_ViewBaseMixin",
	"dojo/domReady!"
	   ], function(declare, lang, array, config, dom, domConstruct, on, template, contentpane,  validtextbox, button, form,
				     dialog, textbox, GuestbookStore, GreetingView, _ViewBaseMixin){
	return declare('guestbookWidget', [_ViewBaseMixin], {
		//	set our template
		templateString: template,

		//	some properties
		guestbookStore: null,
		guestbook_name : 'temp_guestbook',
		greetings: [],

		constructor: function (params) {
            this.guestbook_name = config.guestbook_name;
			//var guestbook_name = this.guestbook_name;
			this.guestbookStore = new GuestbookStore({'guestbook_name': this.guestbook_name });
		},

		postCreate: function(){
			this.inherited(arguments);


			this.own(
				on(this.get_listNode, "click", lang.hitch(this, "getList")),
				on(this.signNode, "click", lang.hitch(this, "signGreeting")),
				on(this.delete_allNode, "click", lang.hitch(this, "deleteAll")),
				on(this.ok_detailNode, "click", lang.hitch(this, "hidePopup"))
			);
		},

		getList: function() {
			this.deleteAll();
			var guestbook_name = dijit.byId('guestbook').get('value');
			this.guestbookStore.getGreetings().then(lang.hitch(this, function(result){
				var greetings = dom.byId('greetingContainer');
				var list = result['object_list']['greetings'];
				if (list.length > 0){
					array.forEach(list, lang.hitch(this, function(greeting, i){

						data = {
							guestbookWidget: this,
							guestbook_name: guestbook_name,
							id: greeting.id,
							author: greeting.author,
							content: greeting.content
						}
						var widget = new GreetingView(data);
						widget.placeAt(greetings)
						widget.startup();
						console.log(this.greetings);
					}));
					if(config.isAdmin) {
						dojo.style(this.delete_divNode, 'display', '');
					}
				}
			}));

		},

		hidePopup: function(){
			this.detail_dialogNode.hide();
		},


		signGreeting: function() {
			postData = {
					guestbook_name: this.guestbook_nameNode.get('value'),
					greeting_message: this.content_dialog_signNode.get('value')
				}
			this.guestbookStore.signGreeting(postData);
		},

		deleteAll: function() {
			dojo.query('.greetingWidget').forEach(function(node){
				dijit.byNode(node).deleteWidget(); // destroy ID
				domConstruct.destroy(node); // destroy innerHTML
			});
		}

	});
});;