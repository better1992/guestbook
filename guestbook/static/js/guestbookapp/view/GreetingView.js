define([
		"dojo/_base/declare",
		"dojo/_base/lang",
		"dojo/_base/Deferred",
		"dojo/dom",
		"dojo/dom-attr",
		"dojo/dom-style",
		"dojo/cookie",
	    "dojo/when",
		"dojo/request",
		"dojo/on",
		"dojo/store/Memory",
		"dojo/text!./templates/GreetingWidget.html",
		"dijit/form/ValidationTextBox",
		"dijit/form/Button",
		"dijit/form/Form",
		"dijit/Dialog",
		"dijit/form/TextBox",
		"guestbookapp/view/_ViewBaseMixin",
	   ], function(declare, lang, Deferred, dom, domAttr, domstyle, cookie, when, request, on, Memory, template, validtextbox, button, form, dialog, textbox, _ViewBaseMixin){
	return declare("greetingWidget",[_ViewBaseMixin], {
		//	set our template
		templateString: template,

		//	some properties
		id: 123,
		author: 'test@gmail.com',
        content: 'demo',
		guestbook_name: '',
		guestbookStore: null,
		isAdmn: 0,
		currentUser: null,
		guestbookWidget: null,
		dialog: null,
		updated: false,

        constructor: function (params) {
			this.guestbookWidget = params.guestbookWidget
			this.guestbook_name = params.guestbook_name,
            this.author = params.author;
            this.content = params.content;
			this.id = params.id;
			this.guestbookStore = this.guestbookWidget.guestbookStore
			this.tempStore = this.guestbookStore;
        },

		postCreate: function(){
			this.inherited(arguments);

			if (this.isAdmin == 0){
				dojo.style(this.option, 'display', 'None');
			}
            this.own(on(this.delete, 'click', lang.hitch(this, 'deleteWidget')),
					on(this.show_Edit, 'click', lang.hitch(this, 'showEdit')),
					on(this.Cancel_Edit, 'click', lang.hitch(this, 'cancelEdit')),
					on(this.Ok_Edit, 'click', lang.hitch(this, 'okEdit')),
					on(this.show_detail, 'click', lang.hitch(this, 'showDetail')));
		},

		refreshStore: function(){
				this.guestbookStore = this.tempStore;
				//return this.guestbookStore
		},

        deleteWidget: function(){
            this.guestbookStore.remove(this.id);
			this.destroyRecursive();

        },
		showEdit: function(){
				this.contentNode.set('readonly', false);
				dojo.style(this.option, 'display', 'None');
				dojo.style(this.edit_option, 'display', '');
		},

		cancelEdit: function(){
				this.contentNode.set('readonly', true);
				dojo.style(this.edit_option, 'display', 'None');
				dojo.style(this.option, 'display', '');
		},

		okEdit : function() {
			this.cancelEdit();
			putData = {
					id: this.id,
					updated_by: this.currentUser,
					guestbook_name: this.guestbook_name,
					greeting_message: this.contentNode.get('value')
				}
			//console.log(this.id);
			this.guestbookStore.put(putData);

		},

		showDetail: function() {

			when(this.guestbookStore.get(this.id)).then(lang.hitch(this, function (greeting) {

				this.guestbookWidget.ID.innerHTML = greeting['object'].id;
				this.guestbookWidget.guestbook_name_dialog.innerHTML = greeting['object'].guestbook_name;
				this.guestbookWidget.author_dialog.innerHTML = greeting['object'].author;
				this.guestbookWidget.content_dialog.innerHTML = greeting['object'].content;
				this.guestbookWidget.date_dialog.innerHTML = greeting['object'].date;
				this.guestbookWidget.updated_by_dialog.innerHTML = greeting['object'].updated_by;
				this.guestbookWidget.updated_date_dialog.innerHTML = greeting['object'].updated_date;

				console.log(greeting);
			}));

			this.guestbookWidget.detail_dialog.show();
			//console.log(this.guestbookStore);
		}


	});
});