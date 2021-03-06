
import xlrd
from collections import defaultdict
from generatePoaXml import *
import settings as settings 
import re
from xml.dom import minidom

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

# set location of XLS files
XLS_PATH = settings.XLS_PATH

# set numbers of rows and cols in xls files for getting col names and data
ROWS_WITH_COLNAMES = settings.ROWS_WITH_COLNAMES
DATA_START_ROW = settings.DATA_START_ROW

# set a map for kind of information available in related xls files
XLS_FILES = settings.XLS_FILES
COLUMN_HEADINGS = settings.XLS_COLUMN_HEADINGS

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

def entities(function):
	"""
	Convert entities to unicode as a decorator
	"""
	def wrapper(*args, **kwargs):
		value = function(*args, **kwargs)
		return entity_to_unicode(value)
	return wrapper

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
	attribute = get_article_attributes(article_id, "subjects", COLUMN_HEADINGS["subject_areas"])
	return attribute

# organisms table

def get_organisms(article_id):
	attribute = get_article_attributes(article_id, "organisms", COLUMN_HEADINGS["organisms"])
	return attribute

# license table

def get_license(article_id):
	attribute = get_article_attributes(article_id, "license", COLUMN_HEADINGS["license_id"])[0]
	return attribute

# manuscript table

@entities
def get_title(article_id):
	attributes = get_article_attributes(article_id, "manuscript", COLUMN_HEADINGS["title"])
	attribute = attributes[0]
	return attribute

@entities
def get_abstract(article_id):
	attributes = get_article_attributes(article_id, "manuscript", COLUMN_HEADINGS["abstract"])
	attribute = attributes[0]
	return attribute

def get_doi(article_id):
	attribute = get_article_attributes(article_id, "manuscript", COLUMN_HEADINGS["doi"])[0]
	return attribute 

def get_accepted_date(article_id):
	attribute = get_article_attributes(article_id, "manuscript", COLUMN_HEADINGS["accepted_date"])[0]
	return attribute

def get_received_date(article_id):
	attribute = get_article_attributes(article_id, "received", COLUMN_HEADINGS["received_date"])[0]
	return attribute

def get_me_id(article_id):
	attribute = get_article_attributes(article_id, "manuscript", COLUMN_HEADINGS["editor_id"])[0]
	return attribute

@entities
def get_me_last_nm(article_id):
	attribute = get_article_attributes(article_id, "manuscript", COLUMN_HEADINGS["editor_last_name"])[0]
	return attribute

@entities
def get_me_first_nm(article_id):
	attribute = get_article_attributes(article_id, "manuscript", COLUMN_HEADINGS["editor_first_name"])[0]
	return attribute

@entities
def get_me_middle_nm(article_id):
	attribute = get_article_attributes(article_id, "manuscript", COLUMN_HEADINGS["editor_middle_name"])[0]
	return attribute

@entities
def get_me_institution(article_id):
	attribute = get_article_attributes(article_id, "manuscript", COLUMN_HEADINGS["editor_institution"])[0]
	return attribute 

@entities
def get_me_department(article_id):
	attribute = get_article_attributes(article_id, "manuscript", COLUMN_HEADINGS["editor_department"])[0]
	return attribute

@entities
def get_me_country(article_id):
	attribute = get_article_attributes(article_id, "manuscript", COLUMN_HEADINGS["editor_country"])[0]
	return attribute

def get_ethics(article_id):
	"""
	needs a bit of refinement owing to serilaising of data by EJP
	"""
	attribute = get_article_attributes(article_id, "manuscript", COLUMN_HEADINGS["ethics"])[0]
	return attribute 

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

@entities
def get_author_last_name(article_id, author_id):
	attribute = get_author_attribute(article_id, author_id, COLUMN_HEADINGS["author_last_name"])
	return attribute 

@entities
def get_author_first_name(article_id, author_id):
	attribute = get_author_attribute(article_id, author_id, COLUMN_HEADINGS["author_first_name"])
	return attribute 

@entities
def get_author_middle_name(article_id, author_id):
	attribute = get_author_attribute(article_id, author_id, COLUMN_HEADINGS["author_middle_name"])
	return attribute 

@entities
def get_author_institution(article_id, author_id):
	attribute = get_author_attribute(article_id, author_id, COLUMN_HEADINGS["author_institution"])
	return attribute 

@entities
def get_author_department(article_id, author_id):
	attribute = get_author_attribute(article_id, author_id, COLUMN_HEADINGS["author_department"])
	return attribute 

@entities
def get_author_city(article_id, author_id):
	attribute = get_author_attribute(article_id, author_id, COLUMN_HEADINGS["author_city"])
	return attribute 

@entities
def get_author_country(article_id, author_id):
	attribute = get_author_attribute(article_id, author_id, COLUMN_HEADINGS["author_country"])
	return attribute 

def get_author_state(article_id, author_id):
	attribute = get_author_attribute(article_id, author_id, COLUMN_HEADINGS["author_state"])
	return attribute

def get_author_conflict(article_id, author_id):
	attribute = get_author_attribute(article_id, author_id, COLUMN_HEADINGS["author_conflict"])
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

def middle_name_initials(middle_name):
	"""
	Given a middle name value parse it to middle initials
	Example inputs:  S, S., Smith, Smith Doe, Smith-Doe, S-D, S D, SD, S.D., S. D.
	Example outputs: S, S,  S,     SD,        S-D,       S-D, SD,  SD, SD,   SD
	"""
	initials = ""
	# Keep only uppercase characters and hyphens
	if middle_name:
		char_list = re.findall("[A-Z]|\-", str(middle_name))
		initials = "".join(char_list)
	
	if initials == "":
		return None
	return initials

def parse_ethics(ethic):
	"""
	Given angle bracket escaped XML string, parse
	animal and human ethic comments, and return
	a list of strings if involved_comments tag
	is found. Boiler plate prefix added too.
	"""
	
	ethics = []
	
	# Decode escaped angle brackets
	ethic_xml = decode_brackets(ethic)
	
	# Parse XML
	encoding = 'utf-8'
	reparsed = minidom.parseString(ethic_xml)
	
	# Extract comments
	for ethic_type in 'animal_subjects','human_subjects':
		ethic_node = reparsed.getElementsByTagName(ethic_type)[0]
		for node in ethic_node.childNodes:
			if node.nodeName == 'involved_comments':
				text_node = node.childNodes[0]
				ethic_text = text_node.nodeValue
				
				# Add boilerplate
				if ethic_type == 'animal_subjects':
					ethic_text = 'Animal experimentation: ' + ethic_text.strip()
				elif ethic_type == 'human_subjects':
					ethic_text = 'Human subjects: ' + ethic_text.strip()
				
				# Decode unicode characters
				ethics.append(entity_to_unicode(ethic_text))

	return ethics

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
	
