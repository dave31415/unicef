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


def get_table_from_mics_file(table_name):
    wb = read_mics()
    sheet = wb.get_sheet_by_name(table_name)
    return sheet.columns


def parse_mics_breastfeeding(print_data=False, print_headers=False):
    table = get_table_from_mics_file('breastfeeding')
    primary_rows = table[0]
    secondary_rows = table[1]
    primary_columns = [column[0] for column in table]
    secondary_columns = [column[1] for column in table]

    if print_headers:
        items = [primary_rows, secondary_rows, primary_columns, secondary_columns]
        items_names = ['primary_rows', 'secondary_rows', 'primary_columns', 'secondary_columns']

        for item_name, item in zip(items_names, items):

            print '\n\t %s' % item_name
            print line
            for cell in item:
                value = cell.value
                if value.strip():
                    print value

    if print_data:
        print line
        print "\t Data"
        print line

    # create a nested data structure
    # with four nested keys
    d1 = lambda: defaultdict(dict)
    d2 = lambda: defaultdict(d1)
    d3 = lambda: defaultdict(d2)
    d4 = lambda: defaultdict(d3)
    data = d4()

    for column_num, column in enumerate(table):
        primary_row = ''
        secondary_row = ''
        primary_col = ''
        secondary_col = ''

        for cell_num, cell in enumerate(column):
            value = cell.value

            primary_row_this = primary_rows[cell_num].value.strip()
            if primary_row_this:
                primary_row = primary_row_this

            secondary_row_this = secondary_rows[cell_num].value.strip()
            if secondary_row_this:
                secondary_row = secondary_row_this

            primary_col_this = primary_columns[column_num].value.strip()
            if primary_col_this:
                primary_col = primary_col_this

            secondary_col_this = secondary_columns[column_num].value.strip()
            if secondary_col_this:
                secondary_col = secondary_col_this

            if primary_row and secondary_row and primary_col and secondary_col:
                data[primary_row][secondary_row][primary_col][secondary_col] = value
                if print_data:
                    print "%s, %s, %s, %s, value: %s" % (primary_row, secondary_row, primary_col, secondary_col, value)

    return data
