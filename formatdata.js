/* Used to convert the raw csv data into the correct json format 
   for circlepacking */

var d3 = require('d3')
var fs = require('fs')

fs.readFile('table.csv', 'utf-8', function(err, csv) {
	var data = {
			'name' : 'positions',
			'children' : [
				{
					'name' : 'QB',
					'children' : [],
				},
				{
					'name' : 'RB',
					'children' : [],
				},
				{
					'name' : 'WR',
					'children' : [],
				},
				{
					'name' : 'TE',
					'children' : [],
				},
				{
					'name' : 'D/ST',
					'children' : [],
				},
				{
					'name' : 'K',
					'children' : [],
				}
			]
		}
	d3.csv.parse(csv).forEach(function(player) {
		// synchronous function
		var points = parseInt(player.PTS);
		points = Math.max(points, 0); // negative values are screwing it up
		var node = {
			'name' : player.PLAYER,
			'value' : points,
			'stats' : player,
		}
		// make parent node values be some of children values

		data.children[map(player.POS)].children.push(node);
	})

	fs.writeFile('data.json', JSON.stringify(data, null, 4));
})
function map(position) {
	switch (position) {
		case 'QB': return 0;
		case 'RB': return 1;
		case 'WR': return 2;
		case 'TE': return 3;
		case 'D/ST': return 4;
		case 'K': return 5;
	}


}