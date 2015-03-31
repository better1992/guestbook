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
	"dijit/InlineEditBox",
	"dijit/Dialog",
	"dijit/form/TextBox",
	"guestbookapp/view/_ViewBaseMixin",
], function(declare, lang, config, dom, domAttr, domstyle, cookie, when, request, on, Memory, template, validtextbox,
			button, form, inlineEditbox, dialog, textbox, _ViewBaseMixin){
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
		updateBy: '',
		updateDate: '',
		dateCreated: null,

		constructor: function (params) {
			this.guestbook_name = params.guestbook_name;
			this.author = params.author;
			this.content = params.content;
			this.id = params.id;
			this.guestbookWidget = params.guestbookWidget;
			this.guestbookStore = params.guestbookWidget.guestbookStore;
			this.dateCreated = params.dateCreated;
			this.updateDate = 'Updated date: ' + params.updateDate
			this.updateBy = 'Update By: ' + params.updateBy;

		},

		postCreate: function() {
			this.inherited(arguments);

			if (config.isAdmin == 0){
				dojo.style(this.optionNode, 'display', 'None');
			}
			this.own(
				on(this.deleteButton, 'click', lang.hitch(this, 'deleteWidget')),
				on(this.contentEditbox, 'change', lang.hitch(this, 'okEdit'))
			);
		},

		deleteWidget: function(){
			this.guestbookStore.deleteGreeting(this.id);
			this.destroyRecursive();

		},

		okEdit : function() {
			putData = {
				id: this.id,
				updated_by: config.currentUser,
				guestbook_name: this.guestbook_name,
				greeting_message: this.contentEditbox.get('value')
			}
			this.guestbookStore.putGreeting(putData).then(lang.hitch(this, function(){
				this.guestbookWidget.getList();
			}));

		}
	});
});