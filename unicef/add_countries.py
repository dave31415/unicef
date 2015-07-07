from __future__ import print_function
from collections import OrderedDict, defaultdict
from pymongo import MongoClient
import csv
from params import pemfile, awsinstance
import ssl

#Open Mongo instance
#Authentication: http://api.mongodb.org/python/current/examples/authentication.html

client = MongoClient(awsinstance,
	ssl=True,
	ssl_certfile=pemfile)

client.the_database.authenticate("<X.509 derived username>",
	mechanism='MONGODB-X509')
db = client.unicef

#Push data to Mongdb instance
infile = "iso3166alpha3.csv"
fin = open(infile, 'rbU')
csvin = csv.reader(fin, dialect=csv.excel_tab)
headers = csvin.next()
for row in csvin:
	print("{}".format(row))


