'use strict';
 
 var app = app || {};
 
 app.Position = Backbone.Model.extend({
     defaults: function() {
         return {
             as_of_date: "",
             asset_perf: 0,
             asset_value: 0,
             liquidative_value: 0,
             money: 0,
             trades: new app.ColTrade()
         }
     }
 });
 
