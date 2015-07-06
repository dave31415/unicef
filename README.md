# unicef

make a file called params.py in the unicef/unicef directory with the
path to the root and data with lines like this

root_dir = "/Users/davej/TW/unicef"

data_dir = "/Users/davej/TW/unicef/data"

Get the .xlsx file and put it into the data directory
(Note I had to convert from .xsl to .xlsx and changed the name slightly)

Install openpyxl if it is not already installed

https://openpyxl.readthedocs.org/en/latest/

To run tests using nose do (from root of the app):

nosetests tests

Example (run from the root of the app)

from unicef import readers

table = readers.get_table_columns_from_mics_file()

from unicef import parse_table

ht = parse_table.HTable(table)

print ht.__class__

unicef.parse_table.HTable

print ht.row_names()

[u'Total', u'Sex', u'Division', u'Area', u"Mother's education", u'Wealth index quintile', u'Religion of household head']

print ht.column_names()

[u'Children 0-5 months', u'Children 12-15 months', u'Children 20-23 months']

Get a subtable

ht2 = ht('Sex','Children 12-15 months')

print ht.__class__

unicef.parse_table.HTable

print ht2.row_names()

[u'Male', u'Female']

print ht2.column_names()

[u'Percent breastfed (Continued breastfeeding at 1 year) [3]', u'Number of children']

This gets a final value rather than another table

print ht2('Male','Number of children')

780.102085034

You can pretty print the table

h2.p()

or get information on them

h2

 Note that you can use these numbers for indexing without a lot of typing
 these return the same thing

ht2(0,1)

ht2('Male','Number of children')

 There is a special case when there is only a single solumn or row left
 In that case the single column/row picks up a name called '.'
 This allows it to remain a HTable, for example

ht('Total',0)

ht('Total',0)('.',1)








