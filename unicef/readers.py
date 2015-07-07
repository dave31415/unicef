from __future__ import print_function
from params import data_dir
from openpyxl import load_workbook
import xlrd
import glob
import os

line = '-----------------------------'


def get_datafilenames(datadir='', fileextension='xls'):
    datafilenames = glob.glob(os.path.join(datadir, '*.'+fileextension))
    return datafilenames


def get_workbook_from_file(filename, verbose=False):
    print 'reading file: %s' % filename
    wb = xlrd.open_workbook(filename)
    if verbose:
        print '\n\tSheet names'
        print line
        for sheet_name in wb.sheet_names():
            print sheet_name
    return wb


# Get either the named sheet, or the first sheet (if input sheetname is blank)
def get_sheet_from_workbook(wb, sheet_name=''):
    if sheet_name == '':
        sheet = wb.sheet_by_index(0)
    else:
        sheet = wb.sheet_by_name(sheet_name)
    return sheet


#Find all the spss tables in an excel worksheet
def get_spss_tables_from_worksheet(sheet=None):
    tables = []
    tablebounds = [] #start and end point for each table
    for i,col0 in enumerate(sheet.col(0)):
        if col0.value.startswith("Table "):
            tablebounds += [i]
    tablebounds += [sheet.nrows]

    for i in range(len(tablebounds)-1):
        table = get_clean_table(sheet, tablebounds[i], tablebounds[i+1])
        if table != {}:
            tables += [table]

    return tables


#Assumes that all excel files output by SPSS have 1 worksheet, with all tables containined in it
def get_dataset_from_spss_excel(spss_excel_file=''):

    wb = get_workbook_from_file(spss_excel_file)
    sheet = get_sheet_from_workbook(wb)
    tables = get_spss_tables_from_worksheet(sheet)
    return tables


def get_table_columns_from_mics_file(sheet_name=''):
    sheet = get_datasheet_from_mics_file(sheet_name)
    return sheet.columns


#Test/data investigation code only
def sniff_first_column(datafilename):
    wb = get_workbook_from_file(datafilename)
    sheet = get_sheet_from_workbook(wb)
    for x in sheet.col(0):
        if x.value != "": 
            print(x)
    return
