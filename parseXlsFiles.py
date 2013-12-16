import xlrd
wb = xlrd.open_workbook('eLife_query_tool_508.xls')

sh = wb.sheet_by_index(0)

row_with_colnames = 3

col_names = sh.row_values(row_with_colnames)

# traspose into a list, so I can slice the list.
rows = []
for rownum in range(sh.nrows):
	rows.append(sh.row_values(rownum))

print ""
data = rows[4:]
for data_row in data: 
	for index, col in enumerate(col_names):
		print col, " : " ,data_row[index] 
		print ""

# for rownum in range(sh.nrows):
#     print sh.row_values(rownum)
#     print ""