def parse_mics_breastfeeding(print_data=False, print_headers=False):
    table = get_table_columns_from_mics_file('breastfeeding')
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

    primary_row = ''
    primary_col = ''

    for column_num, column in enumerate(table):
        for cell_num, cell in enumerate(column):
            value = cell.value

            primary_row_this = primary_rows[cell_num].value.strip()
            if primary_row_this:
                primary_row = primary_row_this

            secondary_row = secondary_rows[cell_num].value.strip()
            if primary_row == 'Total':
                # special case this since it really has no second level
                secondary_row = 'Total'

            primary_col_this = primary_columns[column_num].value.strip()

            if primary_col_this:
                primary_col = primary_col_this

            secondary_col = secondary_columns[column_num].value.strip()

            cell_has_data = primary_row and secondary_row and primary_col and secondary_col

            if cell_has_data:
                data[primary_row][secondary_row][primary_col][secondary_col] = value
                if print_data:
                    print "%s, %s, %s, %s, value: %s" % (primary_row, secondary_row, primary_col, secondary_col, value)

        primary_row = ''

    return data