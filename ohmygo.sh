# A bash shell script that acts as a makefile
python ff-scraper.py # pull the data - it gets put into table.csv
node formatdata.js # turn the data into a json with the appropriate format for the pack layout
