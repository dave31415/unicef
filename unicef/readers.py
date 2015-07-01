from params import data_dir
from openpyxl import load_workbook


line = '-----------------------------'

def file_names(name=None):
    files = {
        'mics': "%s/03_NU_NutritionBangladeshMICS5_converted.xlsx" % data_dir
    }
    if name is not None:
        return files[name]
    return files


def read_mics():
    mics_file = file_names('mics')
    print mics_file
    wb = load_workbook(filename=mics_file)
    sheet_names = [i.title for i in wb.worksheets]
    print '\n\tSheet names'
    print line
    for sheet_name in sheet_names:
        print sheet_name

    return wb


def get_table_from_mics_file(table_name):
    wb = read_mics()
    sheet = wb.get_sheet_by_name(table_name)
    return sheet.columns


def parse_mics_breastfeeding():
    table = get_table_from_mics_file('breastfeeding')
    primary_rows = table[0]
    secondary_rows = table[1]
    primary_columns = [column[0] for column in table]
    secondary_columns = [column[0] for column in table]

    print '\n\t Primary rows'
    print line
    for primary_row in primary_rows:
        value = primary_row.value
        if value.strip():
            print value

