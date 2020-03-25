'use strict';
 
 var app = app || {};
 
 app.ColTrade = Backbone.Collection.extend({
    model: app.Trade,
    parse: function (lst) {
        var res = _.map(lst, function (n) {
            return {id: n};
        });
        return res;
  }
 });
 
