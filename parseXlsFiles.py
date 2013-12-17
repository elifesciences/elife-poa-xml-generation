
import xlrd
from collections import defaultdict

"""
Provide a thin wrapper around a set of functions
to read data from XLS files. 

Ideally the calling script should not need to know
where the underlying XLS files are, or where in those
files the column names are, we should be able to just
call a function that provides something like

	get_email_from_xls("")


Currently we have the following groups of data:

	author

	licence

	manuscript 

	received 

	subject areas 

We should split our helper functions across these groups of data, and we should make the call
based on the documet manuscript number. 


"""

ROWS_WITH_COLNAMES = 3
DATA_START_ROW = 4
XLS_PATH = "/Users/ian/Dropbox/code/private-code/poa-xls-files/ejp_queries_v1.01/"
## set location of xls files 
XLS_FILES = 	{"authors" : "poa_author_v1.01.xls",
				 "licence" : "poa_license_v1.01.xls",
				 "manuscript" : "poa_manuscript_v1.01.xls",
				 "received" : "poa_received.01.xls",
				 "subjects" : "poa_subject_area_v1.01.xls"}

def set_xls_path(path_type):
	"""
	sets the location of the path to the author xls file 
	returns the path 

	This is the only function where the path the our actual data files 
	are set. 
	"""
	path = XLS_PATH + XLS_FILES[path_type]
	return path 

## general functions for getting data from the XLS file
def get_xls_sheet(table_type):
	path = set_xls_path(table_type)	
	wb = xlrd.open_workbook(path)
	sheet = wb.sheet_by_index(0)
	return sheet 

def get_xls_col_names(table_type):
	sheet = get_xls_sheet(table_type)
	col_names = sheet.row_values(ROWS_WITH_COLNAMES)
	return col_names	

def get_xls_data_rows(table_type):
	sheet = get_xls_sheet(table_type)
	rows = []
	for rownum in range(sheet.nrows):
		rows.append(sheet.row_values(rownum))
	data_rows = rows[DATA_START_ROW:]
	return data_rows

def get_cell_value(col_name, col_names, row):
	"""
	we pass the name of the col and a copy of the col names row in to 
	this fucntion so that we don't have to worry about knowing what the 
	index of a specific col name is. 
	"""
	position = col_names.index(col_name)
	cell_value = row[position]
	return cell_value

def index_table_on_article_id(table_type):
	"""
	return a dict of the XLS file keyed on article_id 

	the name of the manuscript number column is hard wired in this function. 
	"""

	path = set_xls_path(table_type)

	# get the data and the row of colnames 
	data_rows = get_xls_data_rows(table_type)
	col_names = get_xls_col_names(table_type)

	article_index = defaultdict(list)
	for data_row in data_rows:
		article_id = get_cell_value("poa_m_ms_no", col_names, data_row)
		# author_id = get_cell_value("poa_a_id", col_names, data_row)
		article_index[article_id].append(data_row)
		# print article_id, author_id 
	return article_index 

# def index_property_on_article_id(table_type, property_id):
# 	"""
# 	as we are going to be doing a lot of looking up authors by 
# 	author_id and manuscript_id, 
# 	so we are going to make a dict of dicts indexed on manuscript is and then author id 
# 	"""
# 	table_type = table_type
# 	col_names = get_xls_col_names(table_type)
# 	author_table = index_table_on_article_id(table_type)

# 	article_ids = author_table.keys()
# 	article_author_index = {} # this is the key item we will return our of this function 
# 	for article_id in article_ids:
# 		rows = author_table[article_id]
# 		author_index =  defaultdict(list)
# 		for row in rows:
# 			author_id = get_cell_value(property_id, col_names, row)
# 			author_index[author_id] = row 
# 		article_author_index[article_id] = author_index
# 	return article_author_index

def index_authors_on_article_id():
	return index_table_on_article_id("authors")


def index_authors_on_author_id():
	# """
	# as we are going to be doing a lot of looking up authors by 
	# author_id and manuscript_id, 
	# so we are going to make a dict of dicts indexed on manuscript is and then author id 
	# """
	table_type = "authors"
	col_names = get_xls_col_names(table_type)
	author_table = index_authors_on_article_id()

	article_ids = author_table.keys()
	article_author_index = {} # this is the key item we will return our of this function 
	for article_id in article_ids:
		rows = author_table[article_id]
		author_index =  defaultdict()
		for row in rows:
			#author_index = {}
			author_id = get_cell_value("poa_a_id", col_names, row)
			author_index[author_id] = row 
		article_author_index[article_id] = author_index
	return article_author_index

def index_subjects_on_article_id():
	return index_table_on_article_id("subjects")

def index_received_on_article_id():
	return index_table_on_article_id("received")

def index_manuscript_on_article_id():
	return index_table_on_article_id("manuscript")

##functions for abstracting calls to specific data entries 

def get_article_attributes(article_id, attribute_type, attribute_label):
	"""

	"""
	attributes = []
	attribute_index = index_table_on_article_id(attribute_type)
	col_names = get_xls_col_names(attribute_type)
	attribute_rows = attribute_index[article_id]
	for attribute_row in attribute_rows:
		attributes.append(get_cell_value(attribute_label ,col_names, attribute_row))
	return attributes

# subjects table

def get_subjects(article_id):
	subjects = get_article_attributes(article_id, "subjects", "poa_s_subjectarea")
	return subjects

# licence table

def get_licence(article_id):
	licence_id = get_article_attributes(article_id, "licence", "poa_l_license_id")[0]
	return licence_id

# manuscript table

def get_title(article_id):
	titles = get_article_attributes(article_id, "manuscript", "poa_m_title")
	title = titles[0]
	return title

def get_abstract(article_id):
	abstracts = get_article_attributes(article_id, "manuscript", "poa_m_abstract")
	abstract = abstracts[0]
	return abstract

def get_doi(article_id):
	doi = get_article_attributes(article_id, "manuscript", "poa_m_doi")[0]
	return doi 

def get_accepted_date(article_id):
	accepted_date = get_article_attributes(article_id, "manuscript", "poa_m_accepted_dt")[0]
	return accepted_date

def get_me_last_nm(article_id):
	me_last_nm = get_article_attributes(article_id, "manuscript", "poa_m_me_last_nm")[0]
	return me_last_nm

def get_me_first_nm(article_id):
	me_first_nm = get_article_attributes(article_id, "manuscript", "poa_m_me_first_nm")[0]
	return me_first_nm

def get_me_middle_nm(article_id):
	me_middle_nm = get_article_attributes(article_id, "manuscript", "poa_m_me_middle_nm")[0]
	return me_middle_nm

def get_me_org(article_id):
	me_org = get_article_attributes(article_id, "manuscript", "poa_m_me_organization")[0]
	return me_org 

def get_me_department(article_id):
	me_department = get_article_attributes(article_id, "manuscript", "poa_m_me_department")[0]
	return me_department

def get_me_country(article_id):
	me_country = get_article_attributes(article_id, "manuscript", "poa_m_me_country")[0]
	return me_country
	"poa_m_me_country"	

def get_ethics(article_id):
	"""
	needs a bit of refinement owing to serilaising of data by EJP
	"""
	ethics = get_article_attributes(article_id, "manuscript", "poa_m_ethics_note")[0]
	return ethics 

# authors table
def get_author_ids(article_id):
	author_ids = get_article_attributes(article_id, "authors", "poa_a_id")
	return author_ids

def get_author_attribute(article_id, author_id, attribute_name):
	article_author_index = index_authors_on_author_id()
	data_row = article_author_index[article_id][author_id]
	col_names = get_xls_col_names("authors")
	attribute = get_cell_value(attribute_name, col_names, data_row)
	return attribute

def get_author_position(article_id, author_id):
	position = get_author_attribute(article_id, author_id, "poa_a_seq")
	return position

def get_author_email(article_id, author_id):
	email = get_author_attribute(article_id, author_id, "poa_a_email")
	return email 

## conversion functions
def doi2uri(doi):
	""
	uri = "http://dx.doi.org/" + doi
	return uri 

## validation functions
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

if __name__ == "__main__":

	# authors = index_table_on_article_id("subjects")
	# print authors

	# print authors[authors.keys()[-1]]
	# print authors.keys()[-1]
	# print authors.keys()
	# article_author_index = index_authors_on_article_id()
	# subject_index = index_subjects_on_article_id()
	# received_index = index_received_on_article_id()
	# manuscript_index = index_manuscript_on_article_id()
	# print article_author_index[1856.0][9026.0]

	test_article_id = 1856.0

	subjects = get_subjects(test_article_id)
	print subjects

	title = get_title(test_article_id)
	print title 

	abstracts = get_abstract(test_article_id)
	print abstracts

	licence_id = get_licence(test_article_id)
	print licence_id

	author_ids = get_author_ids(test_article_id)
	print author_ids

	for author_id in author_ids:
		author_postion = get_author_position(test_article_id, author_id)
		email = get_author_email(test_article_id, author_id)
		print author_postion, email 


	#1856.0 9026.0
	# # Let's be super pragmatic and lift the core article data from the first data row, be fast now! 
	# first_row = data_rows[0]
	# #
	# manuscript = get_cell_value("ms_no", col_names, first_row)
	# doi = get_cell_value("doi", col_names, first_row)
	# title = get_cell_value("ms_title", col_names, first_row)
	# abstract = get_cell_value("abstract", col_names, first_row)

	# # create a list of authors, we have one per data row
	# authors = []
	# for author_row in data_rows:
	# 	"""
	# 	in this strucutre we only have one address per author
	# 	out data structure can support multiple addresses, but we 
	# 	will only have to deal with on address in this example 
	# 	"""

	# 	# create the author object
	# 	contrib_type = "author" # hard coded, as is not in the XLS file
	# 	#
	# 	last_nm = get_cell_value("last_nm", col_names, author_row)
	# 	first_nm = get_cell_value("first_nm", col_names, author_row)
	# 	auth_id = get_cell_value("p_id", col_names, author_row)
	# 	# 
	# 	author = eLifePOSContributor(contrib_type, last_nm, first_nm)
	# 	author.auth_id = "author-" + `int(auth_id)`

	# 	# create the affiliation object
	# 	aff = ContributorAffiliation()
	# 	organization = get_cell_value("organization", col_names, author_row)
	# 	if check_input(organization, "organization"): aff.institution = organization
	# 	#
	# 	department = get_cell_value("department", col_names, author_row)
	# 	if check_input(department, "department"): aff.department = department
	# 	#
	# 	city = get_cell_value("city", col_names, author_row)
	# 	if check_input(city, "city"): aff.city = city
	# 	#
	# 	country = get_cell_value("country", col_names, author_row)
	# 	if check_input(country, "country"): aff.country = country
	# 	#
	# 	telephone = get_cell_value("telephone", col_names, author_row)
	# 	if check_input(telephone, "telephone"): aff.phone = telephone
	# 	#
	# 	fax = get_cell_value("fax", col_names, author_row)
	# 	if check_input(fax, "fax"): aff.fax = fax
	# 	#
	# 	e_mail = get_cell_value("e_mail", col_names, author_row)
	# 	if check_input(e_mail, "e_mail"): aff.email = e_mail

