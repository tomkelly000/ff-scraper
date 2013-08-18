var d3 = require('d3')
var fs = require('fs')

fs.readFile('teams.json', function(err, json) {
	var data = JSON.parse(json);
	var teams = data.sports[0].leagues[0].teams;

	var colors = {};
	teams.forEach(function(team) {
		colors[team.abbreviation] = '#' + team.color; // hex
	})
	fs.writeFile('colors.json', JSON.stringify(colors, null, 4));
});
