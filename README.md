# Fantasy Football 2013 ESPN Projections scraper

Scraping the [ESPN projections](http://games.espn.go.com/ffl/tools/projections?) for the 2013 fantasy football season to be used for [this data visualization](http://bl.ocks.org/tomkelly000/6214228)

## How to
Execute the script ohmygo.sh and you will have a table.csv file with the data and also a data.json formatted for [d3](d3js.org)'s [pack layout](https://github.com/mbostock/d3/wiki/Pack-Layout)

The python script ff-scraper.py makes the table.csv, and formatdata.js (run with node) turns it into data.json

Using ESPN's web api I also pulled the hex values for each NFL team's primary color