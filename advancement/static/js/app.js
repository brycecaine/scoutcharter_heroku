function test_app() {
	console.log('hi there from app')
}

var app = app || {};

$(function() {
	// $( '#releaseDate' ).datepicker();
    new app.ScoutsView();
});