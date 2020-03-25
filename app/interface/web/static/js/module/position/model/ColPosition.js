'use strict';
 
 var app = app || {};
 
 app.ColPosition = Backbone.Collection.extend({
    model: app.Position,
    // parse: function (lst) {
    //     var res = _.map(lst, function (n) {
    //         return {id: n};
    //     });
    //     return res;
    // }
 });
 
