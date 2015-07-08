'''parse_cring.py: convert an xls output by cringonline.com into mongodb
'''
from __future__ import print_function
from collections import OrderedDict, defaultdict
import pymongo
import xlrd
import readers
from cringparams import data_dir

datasource = "CRINGonline"
cringheadings = ["Status", "UNICEF Region", "ISO3 Code", "Country", 
"Time Period", "Total Data Value", "Total Footnote", "Male Data Value",
"Male Footnote", "Female Data Value", "Female Footnote", "Urban Data Value",
"Urban Footnote", "Rural Data Value", "Rural Footnote", "Poorest Data Value",
"Poorest Footnote", "Second Data Value", "Second Footnote", "Middle Data Value",
"Middle Footnote", "Fourth Data Value", "Fourth Footnote", "Richest Data Value",
"Richest Footnote", "Source", "Page/Table No.", "Preliminary", 
"Reanalyzed", "Source Link", "Comments", "Modified Date", "IHSN Link", 
"Document Link 1", "Document Link 2", "Document Link 3", "Document Link 4", 
"Document Link 5", "Scanned Pages"]

#Get worksheets
datafilenames = readers.get_datafilenames(data_dir, 'xls')
for datafilename in datafilenames: 
	wb = readers.get_workbook_from_file(datafilename)
	for sheetname in wb.sheet_names():
		sheet = readers.get_sheet_from_workbook(wb, sheetname)

#Convert worksheets into dict structures, and upload into mongodb
indicatorname = sheet.cell_value(0,0)
indicatorid = indicatorname[:indicatorname.find(" ")]

