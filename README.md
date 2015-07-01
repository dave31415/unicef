# unicef

make a file called params.py in the unicef/unicef directory with the
path to the root and data like this

root_dir = "/Users/davej/TW/unicef"
data_dir = "/Users/davej/TW/unicef/data"

Get the .xlsx file and put it into the data directory
(Note I had to convert from .xsl to .xlsx and changed the name slightly)

Install openpyxl if it is not already installed
https://openpyxl.readthedocs.org/en/latest/


Example (run from the root of the app)

from unicef import readers

data=readers.parse_mics_breastfeeding()

male_newborns = data['Sex']['Male']['Children 0-5 months']

for k, v in male_newborns.iteritems(): print k.ljust(40),v

The result should be...

Percent exclusively breastfed [1]        55.9124910129

Number of children                       973.916536295

Percent predominantly breastfed [2]      70.3852203885


