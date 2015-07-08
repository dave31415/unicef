from __future__ import print_function
from pymongo import MongoClient
import csv
from params import pemfile, awsinstance, awsport

#Open Mongo instance
#Authentication: http://api.mongodb.org/python/current/examples/authentication.html

client = MongoClient(awsinstance, int(awsport))
db = client.unicef
collection = db.cring

#Push data to Mongdb instance
infile = "iso3166alpha3.csv"
fin = open(infile, 'rbU')
csvin = csv.reader(fin, delimiter=",", dialect=csv.excel_tab)
headers = csvin.next()
for row in csvin:
	print("{}".format(row))
	record = {}
	if row[0] != '':
		record['UNICEF Region'] = row[0].encode('utf-8')
	if row[1] != '':
		record['ISO3 code'] = row[1].encode('utf-8')
	if row[2] != '':
		record['Country'] = row[2].encode('utf-8')
	db.iso3_country.insert_one(record)

