'use strict';
 
 var app = app || {};
 
 app.AlertView = Backbone.View.extend({
    tagName: 'div',
    className: "alert fade",
    template: ["<a href=\"#\" data-dismiss=\"alert\" class=\"close\">&times;</a>", "<strong><%= title %></strong>", "<%= message %>"].join("\n"),
    events: {
    },
    initialize: function(options){
        _.bindAll(this, "render", "remove");

        this.template = _.template(this.template);

        if (options) {
            this.alert = options.alert || "info";
            this.title = options.title || "";
            this.message = options.message || "";
            this.fixed = options.fixed || false;
        }
    },
    render: function(){
    var that = this,
				output = this.template({ title: this.title, message: this.message });

			this.$el.addClass("alert-" + this.alert).html(output).alert();

			if (this.fixed) {
				this.$el.addClass("fixed");
			}

			window.setTimeout(function () {
				that.$el.addClass("in");
			}, 20);

			return this;
    },
     remove: function () {
			var that = this;

			this.$el.removeClass("in");

			window.setTimeout(function () {
				that.$el.remove();
			}, 1000);
		},
 });
 
app.AlertView.show = function (title, message, alertType) {
		var alert = new app.AlertView({
			alert: alertType,
			title: title,
			message: message,
			fixed: true
		});

		$(document.body).append(alert.render().el);

		window.setTimeout(function () {
			alert.remove();
		}, 8000);

		return alert;
	};
