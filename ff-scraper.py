''' Scrape the projections for the 2013 fantasy football season from ESPN '''

import urllib2
from bs4 import *
import htmltablescraper

''' return the data from the given page '''
def scrape_data(url):
	try:
		page = urllib2.urlopen(url)
	except:
		return

	soup = BeautifulSoup(page.read())
	table = soup.find('table', {'id' : 'playertable_0'}) # unique identifier for the table
	table = fix_table(table, soup)
	return htmltablescraper.table2array(table)

''' Change the player, team, pos cell to 3 cells and remove the top unneeded top row '''
def fix_table(table, soup):
	table.find('tr').extract() # remove the first row, the big table head
	# change the header to include 4 cells instead of 1
	table.find('td').nextSibling.extract()
	'''inj = soup.new_tag('td')
	inj.string = 'INJ'
	table.td.insert_after('td')'''
	pos = soup.new_tag('td')
	pos.string = 'POS'
	table.td.insert_after(pos)
	team = soup.new_tag('td')
	team.string = 'TEAM'
	table.td.insert_after(team)
	player = soup.new_tag('td')
	player.string = 'PLAYER'
	table.td.insert_after(player)

	# change the rest of the table to match the head
	rows = table.findAll('tr', {'class' : 'pncPlayerRow'})
	for row in rows:
		info = row.find('td').nextSibling.extract()
		link = info.a.extract() # the player's name is a hyperlink
		info = info.contents

		'''inj = soup.new_tag('td')
		inj.string = ' '
		if len(info) > 1: # some sort of injury status
			if info[1].span:
				inj.string = info[1].span.string
		print inj.string
		row.td.insert_after(inj)'''

		info = info[0].split(' ') # team and position are separated by whitespace after a comma
		if len(info) > 1:
			info = info[1]
		else: # hacky way of handling D/ST
			info = info[0]
			info = link.string.split()[0] + info
		info = info.split()
		pos = soup.new_tag('td')
		pos.string = info[1]
		row.td.insert_after(pos)
		team = soup.new_tag('td')
		team.string = info[0]
		row.td.insert_after(team)
		player = soup.new_tag('td')
		player.string =  link.string
		row.td.insert_after(player)

	return table

''' Change the cell into 3 cells: the player, team, and position '''
def convert_cell(cell):
	cell.replaceWith('<td>' + cell.a.string + '</td>' + '<td></td><td></td>')

''' get the url of the next set of players '''
def get_url(index):
	return 'http://games.espn.go.com/ffl/tools/projections?&startIndex=' + str(index)

index = 0 # the index in the projections to scrape from

data = []
while index < 1336:
	page_data = scrape_data(get_url(index))
	index += 40 # ESPN lists 40 per page
	if not page_data: # read through all the pages
		break

	if len(data) > 0: # the first row of each new set of data is the same header
		page_data.pop(0) # so remove it all but the first time

	data.extend(page_data)

htmltablescraper.array2csv(data, '.')