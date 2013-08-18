''' Reads tables from html pages like on the cdc website. '''

import urllib2
from bs4 import *
import sys
import os

''' Takes a url and makes a directory called dname with a csv for
    every table in the html '''
def url2csvs(url, dname='', bytitle=False):
    try:
        html = urllib2.urlopen(url)
    except:
        sys.stderr.write('Could not open ' + url)
        return

    soup = BeautifulSoup(html.read())
    tables = soup('table')
    
    # No tables so we don't want to make a new directory
    if not tables:
        return

    # Makes the directory names the title of the webpage
    if bytitle:
        dname = soup.title.string
        
    # Make new directory if one was specified, otherwise use current directory
    # If directory already exists it is used
    if dname:
        getdir(dname)
    else:
        # Ask user for directory name
        dname = raw_input(
    "Enter directory name or press enter to use current working directory: ")
        if not dname:
            dname = os.getcwd()
        else:
            getdir(dname)
        
    count = 1
    for table in tables:
        array = table2array(table)
        array2csv(array, dname, count) # puts the csv in dname at index count
        count+=1


''' Takes a bs4.element table and turns it into a 2d array '''
def table2array(table):
    rows = table('tr')
    width = getTableWidth(rows)
    array = [[None for i in range(width)]
              for j in range(getTableHeight(rows))]
    i = j = 0 # i is row index, j is col index
    for row in rows:
        cells = row(True, recursive=False) # Get only direct children tags
        for cell in cells:
            # find empty slot - if table is valid it will never run over
            while array[i][j] and j < width:
                j+=1
            # slot hasn't been filled yet
            # fill the span with a whitespace
            rowspan = getRowSpan(row, cell)
            colspan = getColSpan(row, cell)
            for rowOffset in range(rowspan):
                for colOffset in range(colspan):
                    array[i + rowOffset][j + colOffset] = ' '
            # replace top left cell with actual value with commas removed
            array[i][j] = cell.get_text(strip=True).replace(',', '')
            # move over to next slot in row
            j += colspan
        # move to next row
        i+=1
        j = 0
    return array
            

''' Takes an array and puts a csv in dname '''
def array2csv(array, dname, count=''):
    import codecs
    csv = codecs.open(dname + '/table' + str(count) + '.csv', 'w', 'utf-8')
    for row in array:
        csv.write(','.join(row))
        csv.write('\n')
                  

''' Makes a new directory with the specified name, 
    uses it if it already exists'''
def getdir(dname):
    if not os.path.exists(dname):
        os.makedirs(dname)

''' Return the width of the table with rows=rows '''
def getTableWidth(rows):
    width = 0
    cells = rows[0](True, recursive=False) # Get only direct children tags
    # Scan through row adding up colspans
    for cell in cells:
        width += getColSpan(rows[0], cell)
    return width

''' Return the height of the table with rows=rows '''
def getTableHeight(rows):
    return len(rows)

''' Return the rowspan of the cell in row=row'''
def getRowSpan(row, cell):
    if cell in (row.select('td[rowspan]') + row.select('th[rowspan]')):
        return int(cell['rowspan'].strip())
    # doesn't have property; defaults to 1
    return 1

''' Return the colspan of the cell in row=row'''
def getColSpan(row, cell):
    if cell in (row.select('td[colspan]') + row.select('th[colspan]')):
        return int(cell['colspan'].strip())
    # doesn't have property; defaults to 1
    return 1

