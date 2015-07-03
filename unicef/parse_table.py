from collections import OrderedDict, defaultdict


def print_cell(cell):
    info = (cell.address, cell.value, cell.merged, cell.data_type)
    print 'address: %s, value: %s, merged: %s, data_type: %s' % info


def get_unmerged_table_rows(table):
    row_index = []
    rows = []
    for i, cell in enumerate(table[0]):
        if cell.value.strip() and not cell.merged:
            rows.append(cell)
            row_index.append(i)
    return rows, row_index


def get_unmerged_table_columns(table):
    column_index = []
    columns = []
    for i, column in enumerate(table):
        cell = column[0]
        if cell.value.strip() and not cell.merged:
            columns.append(cell)
            column_index.append(i)

    return columns, column_index


def get_rc_structure(rc, rc_index, n_rc_all):
    # get structure for either row or column
    # (hence rc)
    rc_names = [x.value for x in rc]
    lookup = OrderedDict()
    n_rc = len(rc)
    for i in xrange(n_rc):
        rc_name = rc_names[i]
        rc_idx = rc_index[i]
        if i < n_rc-1:
            index_end = rc_index[i+1]-1
        else:
            index_end = n_rc_all-1

        lookup[rc_name] = {'index_start': rc_idx, 'index_end': index_end}
    return lookup


def get_row_col_structure(table):
    rows, row_index = get_unmerged_table_rows(table)
    columns, column_index = get_unmerged_table_columns(table)
    n_columns_all = len(table)
    n_rows_all = len(table[0])
    row_lookup = get_rc_structure(rows, row_index, n_rows_all)
    column_lookup = get_rc_structure(columns, column_index, n_columns_all)
    return row_lookup, column_lookup


class HTable():
    # Class for a hierarchical table
    def __init__(self, table):
        self.row_lookup, self.column_lookup = get_row_col_structure(table)
        self.table = table
        self.verbose = True

    def row_names(self):
        return self.row_lookup.keys()

    def column_names(self):
        return self.column_lookup.keys()

    def _index(self, row_name, column_name):
        # allow integer indexing as well
        # rather than by name (less typing)
        if isinstance(row_name, int):
            row_name = self.row_names()[row_name]
        if isinstance(column_name, int):
            column_name = self.column_names()[column_name]

        if self.verbose:
            print '\n-------------------------------------------'
            print 'selected'
            print "Row name:     %s" % row_name
            print "Column name:  %s" % column_name
            print '-------------------------------------------\n'

        if row_name not in self.row_names():
            return None
        if column_name not in self.column_names():
            return None

        row_start = self.row_lookup[row_name]['index_start']
        row_end = self.row_lookup[row_name]['index_end']

        column_start = self.column_lookup[column_name]['index_start']
        column_end = self.column_lookup[column_name]['index_end']

        if (row_start == row_end) and (column_start == column_end):
            #a final value, not another table
            final_value = self.table[column_start][row_start].value
            return final_value

        # make a mutable version of the table (which is a tuple of tuples)
        table = [list(column) for column in self.table]

        columns_to_keep = set(range(len(table)))
        columns_to_keep.remove(0)

        for column_name_this in self.column_names():
            if column_name_this == column_name:
                #don't remove the column you want to keep, just other ones
                continue
            column_start = self.column_lookup[column_name_this]['index_start']
            column_end = self.column_lookup[column_name_this]['index_end']
            for column_index in xrange(column_start, column_end+1):
                columns_to_keep.remove(column_index)

        rows_to_keep = set(range(len(table[0])))
        rows_to_keep.remove(0)

        #TODO: remove this repetive code
        for row_name_this in self.row_names():
            if row_name_this == row_name:
                #don't remove the row you want to keep, just other ones
                continue
            row_start = self.row_lookup[row_name_this]['index_start']
            row_end = self.row_lookup[row_name_this]['index_end']
            for row_index in xrange(row_start, row_end+1):
                rows_to_keep.remove(row_index)

        sub_table = []
        for col in columns_to_keep:
            column = table[col]
            row = []
            for row_index in rows_to_keep:
                row.append(column[row_index])
            sub_table.append(row)

        # Trick to make it work when there is either
        # a single column or row
        # Gives that single row or column
        # a name "." which keeps it an HTable
        # I *think* this works, needs more tests

        if len(columns_to_keep) == 2:
            sub_table[1][0].value = '.'
            sub_table[1][0].merged = False

        if len(rows_to_keep) == 2:
            sub_table[0][1].value = '.'
            sub_table[0][1].merged = False

        ret_value = HTable(sub_table)
        n_row = len(ret_value.row_names())
        n_col = len(ret_value.column_names())
        if self.verbose:
            dims = (n_row, n_col)
            print '\nReturning another HTable with %s rows and %s columns' % dims
        return ret_value

    def __call__(self, *args, **kwargs):
        # Makes the object callable without having to
        # use the _index() method
         return self._index(*args, **kwargs)

    def _info(self):
        short_line = '--------------'
        row_names = [str(i)+' - '+j for i,j in enumerate(self.row_names())]
        col_names = [str(i)+' - '+j for i,j in enumerate(self.column_names())]
        row_line = "\nRows: \n%s\n%s" % (short_line, "\n".join(row_names))
        col_line = "\n\nColumns: \n%s\n%s" % (short_line, "\n".join(col_names))
        return row_line+col_line

    def __repr__(self):
        return self._info()

    def _transpose(self):
        # rearranges columns of rows to rows of columns
        # and takes the 'value'
        # only used for printing
        trans_table = defaultdict(list)
        for column in self.table:
            for row_num, cell in enumerate(column):
                trans_table[row_num].append(cell.value)
        return [kv[1] for kv in sorted(trans_table.items())]

    def _print(self):
        # pretty printing the table
        # could be improved
        str_length = 15
        just_length = str_length+1
        for row in self._transpose():
            row_string = [str(i)[0:str_length].ljust(just_length) for i in row]
            print ' | '.join(row_string)

    def p(self):
        self._print()