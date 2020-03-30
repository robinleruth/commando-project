'use strict';
 
 var app = app || {};
 
 app.ReportingView = Backbone.View.extend({
    template: _.template($('#reporting_template').html()),
    tagName: 'div',
    className: '',
    events: {
        'click .launch': 'compute',
        'click .download': 'download',
        'blur input': 'saveChange',
        'blur select': 'saveChange',
        'click .switch_graph': 'switchGraph',
    },
    initialize: function(){
        this.listenTo(this.model, 'change', this.render);
        this.listenTo(this.model, 'destroy', this.remove);
        this.listenTo(this.model, 're-render', this.render);
        this.candle = true;

        this.render();
    },
    render: function(){
        this.$el.html(this.template(this.model.toJSON()));
        var file_path = "/static/graph/";
        file_path = file_path + this.model.get('base_100_file_name');
        var img_dom = "<div class='matplotlib_graph' style='display: none;'><img src='" + file_path + "' alt='Image' height='400' width='600'></div>";
        this.$('.b100_image').children().remove();
        if(this.model.get('positions').length > 0){
            var graphView = new app.GraphView({array: this.model.get('positions')});
            this.$('.b100_image').append(graphView.render().el);
            mainjs();
        }
        this.$('.b100_image').append(img_dom);
        this.populateSelects();
        return this;
    },
     compute: function(){
         this.model.compute();
         (function(that){
            setTimeout(function(){
                that.populateSelects();
            }, 1000);
         })(this);
     },
     saveChange: function(e){
         var attributeToChange = e.currentTarget.classList[0];
         var value = e.currentTarget.value;
         var j = {};
         j[attributeToChange] = value;
         this.model.save(j);
     },
     populateSelects: function(){
         this.populateSelect('strategy', 'get_available_strategies');
         this.populateSelect('ptf_type', 'get_ptf_type');
         this.populateSelect('stock', 'get_available_stock');
     },
     populateSelect: function(item, url){
         let dropdown = this.$('.' + item);
         dropdown.empty();
         dropdown.append('<option selected="true" disabled></option>');
         dropdown.prop('selectedIndex', 0);
         url = config.helper_url + url;
         let value = this.model.get(item);
         if(item in this.selectMapping){
                $.each(this.selectMapping[item], function (key, entry) {
                    dropdown.append($('<option></option>').attr('value', entry).text(entry));
                    if(value === entry){
                        dropdown.prop('selectedIndex', key + 1);
                    }
                });
         }else{
             this.selectMapping[item] = [];
             (function(that){
                $.getJSON(url, function (data) {
                    $.each(data, function (key, entry) {
                        dropdown.append($('<option></option>').attr('value', entry).text(entry));
                        that.selectMapping[item].push(entry);
                        if(value === entry){
                            dropdown.prop('selectedIndex', key + 1);
                        }
                    });
                });
             })(this);
         }
     },
     selectMapping: {},
     download: function(){
         this.model.download();
     },
     switchGraph: function(){
         this.candle = !this.candle;
         if(this.candle) {
             this.$('.matplotlib_graph').css('display', 'none');
             this.$('.candle_graph').css('display', 'block');
         } else {
             this.$('.matplotlib_graph').css('display', 'block');
             this.$('.candle_graph').css('display', 'none');
         }
     }
 });
 
