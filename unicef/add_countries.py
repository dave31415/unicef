from __future__ import print_function
from collections import OrderedDict, defaultdict
import pymongo
import csv
from params import pemfile, awsinstance

#Push data to Mongdb instance
infile = "iso3166alpha3.csv"
fin = open(infile, 'rbU')
csvin = csv.reader(fin, dialect=csv.excel_tab)
headers = csvin.next()
for row in csvin:
	print("{}".format(row))

