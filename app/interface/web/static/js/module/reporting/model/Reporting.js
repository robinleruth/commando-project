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
             start_date: "2000-01-03",
             end_date: "2021-04-12",
             stock: "MOCK",
             strategy: "RANDOM_SIGNAL",
             ptf_type: "SHORT_ALLOWED",
             params: [42, 252],
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
        // this.set('params', JSON.stringify(this.get('params')));
        var j = this.toJSON();
        console.log(j);
        // this.set('params', JSON.parse(this.get('params')));
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
                    try{
                        app.AlertView.show('Reporting', status + ' : ' + xhr.responseJSON['detail'], 'danger');
                    }
                    catch(e){
                        app.AlertView.show('Reporting', status + ' : ' + errorThrown, 'danger');
                    }
                    console.log(xhr);
                }
            });
        })(this);
    },
     download: function(){
         var data = this.get('positions');
         var headers = Object.keys(data[0]);
         data.forEach(r => {
             r.positions = JSON.stringify(r.positions);
         });
         var f = function(arr){
             var to_ret = [];
             headers.forEach(elem => {
                 to_ret.push(arr[elem]);
             });
             return to_ret;
         }
         data = data.map(x => f(x));
         data.unshift(headers);
         var n = function(arr){
             var a = '';
             arr.forEach(elem => {
                 a = a + ',' + String(elem);
             });
             return a;
         }
         data = data.map(x => n(x));
         data = data.join('\n');
         var blob = new Blob([data], {type: 'text/csv'});
         var href = window.URL.createObjectURL(blob);
         var link = document.createElement('a');
         link.setAttribute('href', href);
         link.setAttribute('download', 'Positions.csv');
         link.click();
     }
 });
 
