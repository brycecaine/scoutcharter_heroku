function test_models() {
	console.log('hi there from models')
}

var app = app || {};

app.Scout = TastypieModel.extend({
    defaults: {
		// user: 'test',
		// birth_date: 'test date',
		patrol: 'test patrol',
		rank: 'test rank',
		phone_number: 'test phone_number'
    },

    parse: function( response ) {
	    response.id = response._id;
	    return response;
	}
});