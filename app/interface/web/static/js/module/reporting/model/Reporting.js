'use strict';
 
 var app = app || {};
 
 app.Reporting = Backbone.Model.extend({

    parse: function(response) {
        for(var key in response){
            if(_.isArray(response[key])){
                response[key] = new app.ColPosition(response[key], {parse: true});
            }
        }
        return response;
    },
     sync: function(){
        return null;
     },
     defaults: function(){
         return {
             stock: "AAPL",
             strategy: "RANDOM_SIGNAL",
             ptf_type: "SHORT_ALLOWED",
             params: [],
             transaction_fee: 0,
             initial_capital: 1000,
             take_profit: 0,
             stop_loss: 0,
             base_100_file_name: "string.png",
             value_at_risk: 0,
             max_drawdown: 0,
             volatility: 0,
             sharpe_ratio: 0,
             positions: new app.ColPosition()
         }
     },
     compute: function(){
        app.AlertView.show('Reporting', 'Launching...');
        // this.toFormat();
        var j = this.toJSON();
        // this.toVisual();
        (function(model){
            $.ajax({
                url: config.api_url + 'backtester_controller',
                type: 'POST',
                data: JSON.stringify(j),
                contentType: 'application/json',
                success: function(data){
                    app.AlertView.show('Reporting', 'Done!');
                    model.save(data, {parse: true});
                    // model = new app.Reporting(data, {parse: true});
                    // app.reporting = new app.Reporting(data, {parse: true});
                    // model.toVisual();
                },
                error: function(xhr, status, errorThrown){
                    app.AlertView.show('Reporting', status + ' : ' + errorThrown, 'danger');
                }
            });
        })(this);
    },
 });
 
