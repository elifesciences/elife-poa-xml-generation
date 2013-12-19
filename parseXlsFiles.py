
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

	license

	manuscript 

	received 

	subject areas 

We should split our helper functions across these groups of data, and we should make the call
based on the documet manuscript number. 

TODO: parse out the handling editor information
TODO: parse out the ethics information 

"""

ROWS_WITH_COLNAMES = 3
DATA_START_ROW = 4
XLS_PATH = "/Users/ian/Dropbox/code/private-code/poa-xls-files/ejp_queries_v1.04/"
## set location of xls files 
XLS_FILES = 	{"authors" : "poa_author_v1.04.xls",
				 "license" : "poa_license_v1.04.xls",
				 "manuscript" : "poa_manuscript_v1.04.xls",
				 "received" : "poa_received.04.xls",
				 "subjects" : "poa_subject_area_v1.04.xls",
				 "organisms": "poa_research_organism_v1.04.xls"}

COLUMN_HEADINGS = {"author_position" : "poa_a_seq",
					"subject_areas" : "poa_s_subjectarea",
					"license_id" : "poa_l_license_id",
					"title" : "poa_m_title",
					"abstract" : "poa_m_abstract",
					"doi" : "poa_m_doi",
					"accepted_date" : "poa_m_accepted_dt",
					"editor_last_name" : "poa_m_me_last_nm",
					"editor_first_name" : "poa_m_me_first_nm",
					"editor_middle_name" : "poa_m_me_middle_nm",
					"editor_institution" : "poa_m_me_organization", 
					"editor_department" : "poa_m_me_department", 
					"editor_country" : "poa_m_me_country",
					"ethics" : "poa_m_ethics_note",
					"author_id" : "poa_a_id",
					"email" : "poa_a_email",
					"author_type" : "poa_a_type_cde",
					"dual_corresponding" : "poa_a_dual_corr",
					"author_last_name": "poa_a_last_nm",
					"author_first_name": "poa_a_first_nm",
					"author_middle_name" : "poa_a_middle_nm",
					"author_institution" : "poa_a_organization",
					"author_department" : "poa_a_department",
					"author_city" : "poa_a_city", 
					"author_country" : "poa_a_country",
					"author_state" : "poa_a_state",
					"organisms" : "poa_ro_researchorganism"
				}

def memoize(f):
    """ Memoization decorator for functions taking one or more arguments. """
    class memodict(dict):
        def __init__(self, f):
            self.f = f
        def __call__(self, *args):
            return self[args]
        def __missing__(self, key):
            ret = self[key] = self.f(*key)
            return ret
    return memodict(f)

def get_xls_path(path_type):
	"""
	sets the location of the path to the author xls file 
	returns the path 

	This is the only function where the path the our actual data files 
	are set. 
	"""
	path = XLS_PATH + XLS_FILES[path_type]
	return path 

## general functions for getting data from the XLS file
@memoize
def get_xls_sheet(table_type):
	path = get_xls_path(table_type)	
	wb = xlrd.open_workbook(path)
	sheet = wb.sheet_by_index(0)
	return sheet 

@memoize
def get_xls_col_names(table_type):
	sheet = get_xls_sheet(table_type)
	col_names = sheet.row_values(ROWS_WITH_COLNAMES)
	return col_names	

@memoize
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

@memoize
def index_table_on_article_id(table_type):
	"""
	return a dict of the XLS file keyed on article_id 

	the name of the manuscript number column is hard wired in this function. 
	"""

	path = get_xls_path(table_type)

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

@memoize
def index_authors_on_article_id():
	return index_table_on_article_id("authors")

@memoize
def index_authors_on_author_id():
	# """
	# as we are going to be doing a lot of looking up authors by 
	# author_id and manuscript_id, 
	# so we are going to make a dict of dicts indexed on manuscript id and then author id 
	# """
	table_type = "authors"
	col_names = get_xls_col_names(table_type)
	author_table = index_authors_on_article_id()

	article_ids = author_table.keys()
	article_author_index = {}  # this is the key item we will return our of this function 
	for article_id in article_ids:
		rows = author_table[article_id]
		author_index =  defaultdict()
		for row in rows:
			author_id = get_cell_value("poa_a_id", col_names, row)
			author_index[author_id] = row 
		article_author_index[article_id] = author_index
	return article_author_index

##functions for abstracting calls to specific data entries 
@memoize 
def get_article_attributes(article_id, attribute_type, attribute_label):
	attributes = []
	attribute_index = index_table_on_article_id(attribute_type)
	col_names = get_xls_col_names(attribute_type)
	attribute_rows = attribute_index[article_id]
	for attribute_row in attribute_rows:
		attributes.append(get_cell_value(attribute_label ,col_names, attribute_row))
	return attributes

# subjects table

def get_subjects(article_id):
	subjects = get_article_attributes(article_id, "subjects", COLUMN_HEADINGS["subject_areas"])
	return subjects

# organisms table

def get_organisms(article_id):
	organisms = get_article_attributes(article_id, "organisms", COLUMN_HEADINGS["organisms"])
	return organisms

# license table

def get_license(article_id):
	license_id = get_article_attributes(article_id, "license", COLUMN_HEADINGS["license_id"])[0]
	return license_id

# manuscript table

def get_title(article_id):
	titles = get_article_attributes(article_id, "manuscript", COLUMN_HEADINGS["title"])
	title = titles[0]
	return title

def get_abstract(article_id):
	abstracts = get_article_attributes(article_id, "manuscript", COLUMN_HEADINGS["abstract"])
	abstract = abstracts[0]
	return abstract

def get_doi(article_id):
	doi = get_article_attributes(article_id, "manuscript", COLUMN_HEADINGS["doi"])[0]
	return doi 

def get_accepted_date(article_id):
	accepted_date = get_article_attributes(article_id, "manuscript", COLUMN_HEADINGS["accepted_date"])[0]
	return accepted_date

def get_me_last_nm(article_id):
	me_last_nm = get_article_attributes(article_id, "manuscript", COLUMN_HEADINGS["editor_last_name"])[0]
	return me_last_nm

def get_me_first_nm(article_id):
	me_first_nm = get_article_attributes(article_id, "manuscript", COLUMN_HEADINGS["editor_first_name"])[0]
	return me_first_nm

def get_me_middle_nm(article_id):
	me_middle_nm = get_article_attributes(article_id, "manuscript", COLUMN_HEADINGS["editor_middle_name"])[0]
	return me_middle_nm

def get_me_institution(article_id):
	me_org = get_article_attributes(article_id, "manuscript", COLUMN_HEADINGS["editor_institution"])[0]
	return me_org 

def get_me_department(article_id):
	me_department = get_article_attributes(article_id, "manuscript", COLUMN_HEADINGS["editor_department"])[0]
	return me_department

def get_me_country(article_id):
	me_country = get_article_attributes(article_id, "manuscript", COLUMN_HEADINGS["country"])[0]
	return me_country

def get_ethics(article_id):
	"""
	needs a bit of refinement owing to serilaising of data by EJP
	"""
	ethics = get_article_attributes(article_id, "manuscript", COLUMN_HEADINGS["ethics"])[0]
	return ethics 

# authors table
def get_author_ids(article_id):
	author_ids = get_article_attributes(article_id, "authors", COLUMN_HEADINGS["author_id"])
	return author_ids

def get_author_attribute(article_id, author_id, attribute_name):
	article_author_index = index_authors_on_author_id()
	data_row = article_author_index[article_id][author_id]
	col_names = get_xls_col_names("authors")
	attribute = get_cell_value(attribute_name, col_names, data_row)
	return attribute

def get_author_position(article_id, author_id):
	attribute = get_author_attribute(article_id, author_id, COLUMN_HEADINGS["author_position"])
	return attribute

def get_author_email(article_id, author_id):
	attribute = get_author_attribute(article_id, author_id, COLUMN_HEADINGS["email"])
	return attribute 

def get_author_contrib_type(article_id, author_id):
	attribute = get_author_attribute(article_id, author_id, COLUMN_HEADINGS["author_type"])
	return attribute 

def get_author_dual_corresponding(article_id, author_id):
	attribute = get_author_attribute(article_id, author_id, COLUMN_HEADINGS["dual_corresponding"])
	return attribute 

def get_author_last_name(article_id, author_id):
	attribute = get_author_attribute(article_id, author_id, COLUMN_HEADINGS["author_last_name"])
	return attribute 

def get_author_first_name(article_id, author_id):
	attribute = get_author_attribute(article_id, author_id, COLUMN_HEADINGS["author_first_name"])
	return attribute 

def get_author_middle_name(article_id, author_id):
	attribute = get_author_attribute(article_id, author_id, COLUMN_HEADINGS["author_middle_name"])
	return attribute 

def get_author_institution(article_id, author_id):
	attribute = get_author_attribute(article_id, author_id, COLUMN_HEADINGS["author_institution"])
	return attribute 

def get_author_department(article_id, author_id):
	attribute = get_author_attribute(article_id, author_id, COLUMN_HEADINGS["author_department"])
	return attribute 

def get_author_city(article_id, author_id):
	attribute = get_author_attribute(article_id, author_id, COLUMN_HEADINGS["author_city"])
	return attribute 

def get_author_country(article_id, author_id):
	attribute = get_author_attribute(article_id, author_id, COLUMN_HEADINGS["author_country"])
	return attribute 

def get_author_state(article_id, author_id):
	attribute = get_author_attribute(article_id, author_id, COLUMN_HEADINGS["author_state"])
	return attribute 

## conversion functions
def doi2uri(doi):
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

	test_article_id = 1856.0

	subjects = get_subjects(test_article_id)
	print subjects

	title = get_title(test_article_id)
	print title 

	abstracts = get_abstract(test_article_id)
	print abstracts

	license_id = get_license(test_article_id)
	print license_id

	author_ids = get_author_ids(test_article_id)
	print author_ids

	for author_id in author_ids:
		author_postion = get_author_position(test_article_id, author_id)
		email = get_author_email(test_article_id, author_id)
		print author_postion, email 
