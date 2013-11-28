from generatePoaXml import *
import xlrd

"""
read from an xls file
output an xml file


# Gotchas
TODO: currnet XLS does not provide author contrib type TODO: query for author contrib type 
TODO: we need a decision on what we do with middle names, for now we are ignoring them 

"""

## functions for getting data from the XLS file
def get_xls_sheet(path):
	wb = xlrd.open_workbook(path)
	sheet = wb.sheet_by_index(0)
	return sheet 

def get_xls_col_names(path, name_row):
	sheet = get_xls_sheet(path)
	col_names = sheet.row_values(name_row)
	return col_names	

def get_xls_data_rows(path, DATA_START_ROW):
	sheet = get_xls_sheet(path)
	rows = []
	for rownum in range(sheet.nrows):
		rows.append(sheet.row_values(rownum))

	data_rows = rows[DATA_START_ROW:]
	return data_rows

## Helper functions
def doi2uri(doi):
	""
	uri = "http://dx.doi.org/" + doi
	return uri 

def get_cell_value(col_name, col_names, row):
	position = col_names.index(col_name)
	cell_value = row[position]
	return cell_value

def check_phone_number(number):
	if len(number) < 4:
		return False
	else:
		return True

def check_fax_number(number):
	if len(number) < 4:
		return False
	else:
		return True

def check_input(value, input_name):
	"""
	helper function to manage basic data validation,
	e.g. the xls file has whitespace for fax numbers, and in those cases we 
	should omit the fax number. 
	"""
	if input_name == "telephone":
		return check_phone_number(value)
	elif input_name == "fax":
		return check_fax_number(value)
	else:
		return True

if __name__ == "__main__":
	# parse data from the generated XLS file 
	SAMPLE_XLS_PATH = "sample-xls-input/eLife_query_tool_508.xls"
	ROWS_WITH_COLNAMES = 3
	DATA_START_ROW = 4

	data_rows = get_xls_data_rows(SAMPLE_XLS_PATH, DATA_START_ROW)
	col_names = get_xls_col_names(SAMPLE_XLS_PATH, ROWS_WITH_COLNAMES)

	# Let's be super pragmatic and lift the core article data from the first data row, be fast now! 
	first_row = data_rows[0]
	# 
	doi = get_cell_value("doi", col_names, first_row)
	title = get_cell_value("ms_title", col_names, first_row)
	abstract = get_cell_value("abstract", col_names, first_row)

	# create a list of authors, we have one per data row
	authors = []
	for author_row in data_rows:
		"""
		in this strucutre we only have one address per author
		out data structure can support multiple addresses, but we 
		will only have to deal with on address in this example 
		"""

		# create the author object
		contrib_type = "author" # hard coded, as is not in the XLS file
		#
		last_nm = get_cell_value("last_nm", col_names, author_row)
		first_nm = get_cell_value("first_nm", col_names, author_row)
		auth_id = get_cell_value("p_id", col_names, author_row)
		# 
		author = eLifePOSContributor(contrib_type, last_nm, first_nm)
		author.auth_id = "author-" + `int(auth_id)`

		# create the affiliation object
		aff = ContributorAffiliation()
		organization = get_cell_value("organization", col_names, author_row)
		if check_input(organization, "organization"): aff.institution = organization
		#
		department = get_cell_value("department", col_names, author_row)
		if check_input(department, "department"): aff.department = department
		#
		city = get_cell_value("city", col_names, author_row)
		if check_input(city, "city"): aff.city = city
		#
		country = get_cell_value("country", col_names, author_row)
		if check_input(country, "country"): aff.country = country
		#
		telephone = get_cell_value("telephone", col_names, author_row)
		if check_input(telephone, "telephone"): aff.phone = telephone
		#
		fax = get_cell_value("fax", col_names, author_row)
		if check_input(fax, "fax"): aff.fax = fax
		#
		e_mail = get_cell_value("e_mail", col_names, author_row)
		if check_input(e_mail, "e_mail"): aff.email = e_mail

		# add the affiliation to the author
		author.set_affiliation(aff)

		authors.append(author)

	# create an article object
	uri = doi2uri(doi)
	article = eLifePOA(uri, title)

	# add authors to the article
	for author in authors:
		article.add_contributor(author)

	# generate the XML from the article object
	poa_xml = eLife2XML(article)
	print poa_xml.prettyXML()

	# for col_name in col_names: print col_name, # have this line to hand if we want to inspect col names


 