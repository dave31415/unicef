from params import data_dir
from openpyxl import load_workbook
from collections import defaultdict

line = '-----------------------------'


def file_names(name=None):
    files = {
        'mics': "%s/03_NU_NutritionBangladeshMICS5_converted.xlsx" % data_dir
    }
    if name is not None:
        return files[name]
    return files


def read_mics(verbose=False):
    mics_file = file_names('mics')
    print 'reading file: %s' % mics_file
    wb = load_workbook(filename=mics_file)
    sheet_names = [i.title for i in wb.worksheets]
    if verbose:
        print '\n\tSheet names'
        print line
        for sheet_name in sheet_names:
            print sheet_name
    return wb


def get_sheet_from_mics_file(sheet_name):
    wb = read_mics()
    sheet = wb.get_sheet_by_name(sheet_name)
    return sheet


def get_table_columns_from_mics_file(sheet_name='breastfeeding'):
    sheet = get_sheet_from_mics_file(sheet_name)
    return sheet.columns
