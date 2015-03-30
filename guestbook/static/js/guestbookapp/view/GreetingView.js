define([
		"dojo/_base/declare",
		"dojo/_base/lang",
		"dojo/_base/config",
		"dojo/dom",
		"dojo/dom-attr",
		"dojo/dom-style",
		"dojo/cookie",
	    "dojo/when",
		"dojo/request",
		"dojo/on",
		"dojo/store/Memory",
		"dojo/text!./templates/GreetingView.html",
		"dijit/form/ValidationTextBox",
		"dijit/form/Button",
		"dijit/form/Form",
		"dijit/Dialog",
		"dijit/form/TextBox",
		"guestbookapp/view/_ViewBaseMixin",
	   ], function(declare, lang, config, dom, domAttr, domstyle, cookie, when, request, on, Memory, template, validtextbox, button, form, dialog, textbox, _ViewBaseMixin){
	return declare("greetingWidget",[_ViewBaseMixin], {
		//	set our template
		templateString: template,

		//	some properties
		id: 123,
		author: 'test@gmail.com',
		content: 'demo',
		guestbook_name: '',
		guestbookStore: null,
		guestbookWidget: null,

        constructor: function (params) {
			this.guestbookWidget = params.guestbookWidget
			this.guestbook_name = params.guestbook_name,
            this.author = params.author;
            this.content = params.content;
			this.id = params.id;
			this.guestbookStore = this.guestbookWidget.guestbookStore
        },

		postCreate: function(){
			this.inherited(arguments);

			if (config.isAdmin == 0){
				dojo.style(this.optionNode, 'display', 'None');
			}
            this.own(
				on(this.deleteNode, 'click', lang.hitch(this, 'deleteWidget')),
				on(this.show_EditNode, 'click', lang.hitch(this, 'showEdit')),
				on(this.Cancel_EditNode, 'click', lang.hitch(this, 'cancelEdit')),
				on(this.Ok_EditNode, 'click', lang.hitch(this, 'okEdit')),
				on(this.show_detailNode, 'click', lang.hitch(this, 'showDetail'))
			);
		},

        deleteWidget: function(){
            this.guestbookStore.deleteGreeting(this.id);
			this.destroyRecursive();

        },
		showEdit: function(){
				this.contentNode.set('readonly', false);
				dojo.style(this.optionNode, 'display', 'None');
				dojo.style(this.edit_optionNode, 'display', '');
		},

		cancelEdit: function(){
				this.contentNode.set('readonly', true);
				dojo.style(this.edit_optionNode, 'display', 'None');
				dojo.style(this.optionNode, 'display', '');
		},

		okEdit : function() {
			this.cancelEdit();
			putData = {
					id: this.id,
					updated_by: config.currentUser,
					guestbook_name: this.guestbook_name,
					greeting_message: this.contentNode.get('value')
				}
			this.guestbookStore.putGreeting(putData);

		},

		showDetail: function() {
			this.guestbookStore.getGreeting(this.id).then(lang.hitch(this, function (greeting) {
				this.guestbookWidget.IDNode.innerHTML = greeting['object'].id;
				this.guestbookWidget.guestbook_name_dialogNode.innerHTML = greeting['object'].guestbook_name;
				this.guestbookWidget.author_dialogNode.innerHTML = greeting['object'].author;
				this.guestbookWidget.content_dialogNode.innerHTML = greeting['object'].content;
				this.guestbookWidget.date_dialogNode.innerHTML = greeting['object'].date;
				this.guestbookWidget.updated_by_dialogNode.innerHTML = greeting['object'].updated_by;
				this.guestbookWidget.updated_date_dialogNode.innerHTML = greeting['object'].updated_date;
			}));
			this.guestbookWidget.detail_dialogNode.show();
		}


	});
});