'use strict';

var app = app || {};

app.GraphView = Backbone.View.extend({
   template: _.template($('#graph_view_template').html()),
   tagName: 'div',
   className: '',
   events: {
   },
   initialize: function(options){
       this.array = options.array;
   },
   render: function(){
       this.$el.html(this.template());
       genRaw = this.array.map(genType);
       // mainjs();
       return this;
   },
});
