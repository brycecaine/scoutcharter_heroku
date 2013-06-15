function test_collections() {
	console.log('hi there from collections')
}

var app = app || {};

app.Scouts = TastypieCollection.extend({
    model: app.Scout,
    url: '/api/scouts',
    parse: function(response){
    	console.log(response.objects)
    	return response.objects;
	}
});