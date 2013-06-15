function test_views_scout() {
	console.log('hi there from views scout')
}

var app = app || {};

app.ScoutView = Backbone.View.extend({
    tagName: 'div',
    className: 'scoutContainer',
    template: _.template( $( '#scoutTemplate' ).html() ),

    events: {
        'click .delete': 'deleteScout'
    },

    deleteScout: function() {
        //Delete model
        this.model.destroy();

        //Delete view
        this.remove();
    },

    render: function() {
        //this.el is what we defined in tagName. use $el to get access to jQuery html() function
        this.$el.html( this.template( this.model.toJSON() ) );

        return this;
    }
});