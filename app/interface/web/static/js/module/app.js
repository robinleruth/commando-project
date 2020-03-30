'use strict';

var app = app || {};

(function(){
    app.reporting = new app.Reporting();

    app.reporting_view = new app.ReportingView({model: app.reporting, el: '#reporting'});
    $(document).keydown(function(e){
        if(e.keyCode == 13){
            app.reporting_view.compute();
        }
    });

})();
