function test_collections() {
	console.log('hi there from collections')
}

var app = app || {};

app.Scouts = TastypieCollection.extend({
    model: app.Scout,
    url: '/api/v1/scouts'
 //    parse: function(response){
 //    	console.log('thats why')
 //    	return response.objects;
	// }
});