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
], function(declare, lang, array, config, dom, domConstruct, on, template,
			contentpane, validtextbox, button, form,
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
			this.getList();

			this.own(
				on(this.getListButton, "click", lang.hitch(this, "refreshList")),
				on(this.signButton, "click", lang.hitch(this, "sign")),
				on(this.showSignButton, "click", lang.hitch(this, "showSign")),
				on(this.deleteAllButton, "click", lang.hitch(this, "deleteAll")),
				on(this.cancelButton, "click", lang.hitch(this, "hideSign"))
			);
		},

		refreshList: function() {
			dojo.query('.greetingWidget').forEach(function(node){
				dijit.byNode(node).destroyRecursive();
				domConstruct.destroy(node);
			});
			this.getList();
		},

		getList: function() {
			if(!this.guestbookNameTextbox.validate()) {
				alert('Form contains invalid data. Please correct first');
				return false;
			}
			var guestbook_name = this.guestbookNameTextbox.get('value');
			this.guestbookStore.getGreetings({'guestbook_name': guestbook_name}).then(
				lang.hitch(this, function(result){
				var greetings = dom.byId('greetingContainer');
				var list = result['object_list']['greetings'];
				var domFrag = document.createDocumentFragment();
				if (list.length > 0){
					array.forEach(list, lang.hitch(this, function(greeting, i){

						data = {
							guestbookWidget: this,
							guestbook_name: guestbook_name,
							id: greeting.id,
							author: greeting.author,
							content: greeting.content,
							updateDate: greeting.updatedDate,
							updateBy: greeting.updatedBy,
							dateCreated: greeting.dateCreated
						}
						var widget = new GreetingView(data);
						widget.placeAt(domFrag);
					}));
					if(config.isAdmin == "True") {
						dojo.style(this.deleteDivNode, 'display', '');
					}
				}
				domConstruct.place(domFrag, greetings);
				dojo.query('.greetingWidget').forEach(function(node){
					dijit.byNode(node).startup();
				});
			}));

		},

		hideSign: function(){
			dojo.style(this.signOptionNode, 'display', 'None');
		},

		showSign: function() {
			dojo.style(this.signOptionNode, 'display', '');
		},

		sign: function() {
			if(!this.guestbookNameTextbox.validate() || !this.contentSignTextbox.validate()) {
				alert('Form contains invalid data. Please correct first');
				return false;
			}
			postData = {
				guestbook_name: this.guestbookNameTextbox.get('value'),
				greeting_message: this.contentSignTextbox.get('value')
			}
			this.guestbookStore.signGreeting(postData).then(lang.hitch(this, function(){
				this.refreshList();
			}));
			dojo.style(this.signOptionNode, 'display', 'None');
		},

		deleteAll: function() {
			dojo.query('.greetingWidget').forEach(function(node){
				dijit.byNode(node).deleteWidget(); // destroy ID
				domConstruct.destroy(node); // destroy innerHTML
			});
		}

	});
});;