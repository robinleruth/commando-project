'use strict';

var app = app || {};

(function(){
    app.reporting = new app.Reporting();

    app.reporting_view = new app.ReportingView({model: app.reporting, el: '#reporting'});

})();
