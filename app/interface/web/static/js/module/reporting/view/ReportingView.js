'use strict';
 
 var app = app || {};
 
 app.ReportingView = Backbone.View.extend({
    template: _.template($('#reporting_template').html()),
    tagName: 'div',
    className: '',
    events: {
        'click .launch': 'compute',
        'blur input': 'saveChange',
        'blur select': 'saveChange',
    },
    initialize: function(){
        this.listenTo(this.model, 'change', this.render);
        this.listenTo(this.model, 'destroy', this.remove);
        this.listenTo(this.model, 're-render', this.render);

        this.render();
    },
    render: function(){
        this.$el.html(this.template(this.model.toJSON()));
        var file_path = "/static/graph/";
        file_path = file_path + this.model.get('base_100_file_name');
        var img_dom = "<img src='" + file_path + "' alt='Image' height='400' width='600'>";
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
     selectMapping: {}
 });
 
