function test_views_scouts() {
	console.log('hi there from views scouts')
}

var app = app || {};

app.ScoutsView = Backbone.View.extend({
    el: '#scouts',

    initialize: function( initialScouts ) {
    	console.log(initialScouts)
        this.collection = new app.Scouts( initialScouts );
        this.collection.fetch({reset: true});
    	console.log(this.collection)
        this.render();
        
        this.listenTo( this.collection, 'add', this.renderScout );
        this.listenTo( this.collection, 'reset', this.render );
    },

	events: {
	    'click #add':'addScout'
	},

	addScout: function( e ) {
	    e.preventDefault();

	    var formData = {};

	    $( '#addScout div' ).children( 'input' ).each( function( i, el ) {
	        if( $( el ).val() != '' )
	        {
	            formData[ el.id ] = $( el ).val();
	        }
	    });

	    this.collection.add( new app.Scout( formData ) );
	},

    // render scouts by rendering each scout in its collection
    render: function() {
        this.collection.each(function( item ) {
            this.renderScout( item );
        }, this );
    },

    // render a scout by creating a ScoutView and appending the
    // element it renders to the scouts's element
    renderScout: function( item ) {
        var scoutView = new app.ScoutView({
            model: item
        });
        this.$el.append( scoutView.render().el );
    }
});