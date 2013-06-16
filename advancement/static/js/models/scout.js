function test_models() {
	console.log('hi there from models')
}

var app = app || {};

app.Scout = TastypieModel.extend({
    defaults: {
		user: 'test',
		// birth_date: 'test date',
		patrol: 'test patrol',
		rank: 'test rank',
		phone_number: 'test phone_number'
    }
});

app.Rank = TastypieModel.extend({
	defaults: {
		weight: 100,
		name: 'default rank',
		number_required_meritbadges: 0,
		number_optional_meritbadges: 0
	}
})