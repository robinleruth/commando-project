'use strict';
 
 var app = app || {};
 
 app.Trade = Backbone.Model.extend({
     defaults: function(){
         return {
            as_of_date: '', 
            side: '', 
            qty: 0, 
            pos_value: 0, 
            take_profit: 0, 
            stop_loss: 0, 
            initial_pos_value: 0
         }
     }
 });
 
