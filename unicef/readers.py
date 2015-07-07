from params import data_dir
from openpyxl import load_workbook
import glob
import os

line = '-----------------------------'


def get_datafilenames(datadir='', fileextension='xls'):
    datafilenames = glob.glob(os.path.join(datadir, '*.'+fileextension))
    return datafilenames


def read_mics_file(mics_file, verbose=False):
    print 'reading file: %s' % mics_file
    wb = load_workbook(filename=mics_file)
    if verbose:
        sheet_names = [i.title for i in wb.worksheets]
        print '\n\tSheet names'
        print line
        for sheet_name in sheet_names:
            print sheet_name
    return wb

# Get either the named sheet, or the first sheet (if input sheetname is blank)
def get_sheet_from_mics_file(sheet_name=''):
    wb = read_mics_file()
    if sheet_name != '':
        sheet = wb.get_sheet_by_name(sheet_name)
    else:
        sheet = wb.get_sheet_by_name(sheet_name)        
    return sheet


def get_table_columns_from_mics_file(sheet_name=''):
    sheet = get_sheet_from_mics_file(sheet_name)
    return sheet.columns
