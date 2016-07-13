
import csv
from collections import defaultdict
from generatePoaXml import *
import settings as settings
import re
from xml.dom import minidom
import logging

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

logger = logging.getLogger('parseCSV')
hdlr = logging.FileHandler('parseCSV.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

# set location of XLS files
XLS_PATH = settings.XLS_PATH

# set numbers of rows and cols in xls files for getting col names and data
ROWS_WITH_COLNAMES = settings.ROWS_WITH_COLNAMES
DATA_START_ROW = settings.DATA_START_ROW

# set a map for kind of information available in related xls files
XLS_FILES = settings.XLS_FILES
COLUMN_HEADINGS = settings.XLS_COLUMN_HEADINGS

OVERFLOW_XLS_FILES = settings.OVERFLOW_XLS_FILES

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
    logger.info("in get_xls_sheet")
    path = get_xls_path(table_type)
    logger.info(str(path))
    csvreader = csv.reader(open(path, 'rb'), delimiter=',', quotechar='"')
    sheet = []
    for row in csvreader: sheet.append(row)
    # For overflow file types, parse again with no quotechar
    if table_type in OVERFLOW_XLS_FILES:
        csvreader = csv.reader(open(path, 'rb'), delimiter=',', quotechar=None)
        for row in csvreader:
            if csvreader.line_num <= DATA_START_ROW:
                continue
            # Merge cells 3 to the end because any commas will cause extra columns
            row[2] = ','.join(row[2:])
            for index, cell in enumerate(row):
                # Strip leading quotation marks
                row[index] = cell.lstrip('"').rstrip('"')
            try:
                sheet[csvreader.line_num-1] = row
            except IndexError:
                # Last line may not exist so handle the error
                pass
    return sheet

@memoize
def get_xls_col_names(table_type):
    logger.info("in get_xls_col_names")
    logger.info(table_type)
    sheet = get_xls_sheet(table_type)
    logger.info(sheet)
    logger.info(str(ROWS_WITH_COLNAMES))
    for index, row in enumerate(sheet):
        logger.info("in enumerate")
        logger.info(str(index) + " " + str(row))
        logger.debug(str(index) + " " + str(ROWS_WITH_COLNAMES))
        if int(index) == int(ROWS_WITH_COLNAMES):
            return row

@memoize
def get_xls_data_rows(table_type):
    sheet = get_xls_sheet(table_type)
    rows = []
    for row in sheet:
        rows.append(row)
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

    logger.info("in index_table_on_article_id")
    path = get_xls_path(table_type)

    # get the data and the row of colnames
    data_rows = get_xls_data_rows(table_type)
    col_names = get_xls_col_names(table_type)

    # logger.info("data_rows: " + str(data_rows))
    logger.info("col_names: " + str(col_names))

    article_index = defaultdict(list)
    for data_row in data_rows:
        article_id = get_cell_value('poa_m_ms_no', col_names, data_row)
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
        author_index = defaultdict()
        for row in rows:
            author_id = get_cell_value("poa_a_id", col_names, row)
            author_index[author_id] = row
        article_author_index[article_id] = author_index
    return article_author_index

##functions for abstracting calls to specific data entries
@memoize
def get_article_attributes(article_id, attribute_type, attribute_label):
    logger.info("in get_article_attributes")
    logger.info("artilce_id: " + str(article_id) + " attribute_type: " +
                attribute_type + " attribute_label:" +  attribute_label)
    attributes = []
    logger.info("about to generate attribute index")
    attribute_index = index_table_on_article_id(attribute_type)
    logger.info("generated attribute index")
    # logger.info(str(attribute_index))
    logger.info("about to get col_names for colname " + str(attribute_type))
    col_names = get_xls_col_names(attribute_type)
    attribute_rows = attribute_index[str(article_id)]
    for attribute_row in attribute_rows:
        attributes.append(get_cell_value(attribute_label, col_names, attribute_row))
    return attributes

# subjects table

def get_subjects(article_id):
    attribute = get_article_attributes(article_id, "subjects",
                                       COLUMN_HEADINGS["subject_areas"])
    return attribute

# organisms table

def get_organisms(article_id):
    attribute = get_article_attributes(article_id, "organisms",
                                       COLUMN_HEADINGS["organisms"])
    return attribute

# license table

def get_license(article_id):
    attribute = get_article_attributes(article_id, "license",
                                       COLUMN_HEADINGS["license_id"])[0]
    return attribute

# keywords table

def get_keywords(article_id):
    attribute = get_article_attributes(article_id, "keywords",
                                       COLUMN_HEADINGS["keywords"])
    return attribute

# manuscript table

@entities
def get_title(article_id):
    attributes = get_article_attributes(article_id, "title",
                                        COLUMN_HEADINGS["title"])
    attribute = attributes[0]
    return attribute

@entities
def get_abstract(article_id):
    attributes = get_article_attributes(article_id, "abstract",
                                        COLUMN_HEADINGS["abstract"])
    attribute = attributes[0]
    return attribute

def get_doi(article_id):
    attribute = get_article_attributes(article_id, "manuscript",
                                       COLUMN_HEADINGS["doi"])[0]
    return attribute

def get_articleType(article_id):
    attribute = get_article_attributes(article_id, "manuscript",
                                       COLUMN_HEADINGS["articleType"])[0]
    return attribute

def get_accepted_date(article_id):
    attribute = get_article_attributes(article_id, "manuscript",
                                       COLUMN_HEADINGS["accepted_date"])[0]
    return attribute

def get_received_date(article_id):
    attribute = get_article_attributes(article_id, "received",
                                       COLUMN_HEADINGS["received_date"])[0]
    return attribute

def get_receipt_date(article_id):
    attribute = get_article_attributes(article_id, "received",
                                       COLUMN_HEADINGS["receipt_date"])[0]
    return attribute

def get_me_id(article_id):
    attribute = get_article_attributes(article_id, "manuscript",
                                       COLUMN_HEADINGS["editor_id"])[0]
    return attribute

@entities
def get_me_last_nm(article_id):
    attribute = get_article_attributes(article_id, "manuscript",
                                       COLUMN_HEADINGS["editor_last_name"])[0]
    return attribute

@entities
def get_me_first_nm(article_id):
    attribute = get_article_attributes(article_id, "manuscript",
                                       COLUMN_HEADINGS["editor_first_name"])[0]
    return attribute

@entities
def get_me_middle_nm(article_id):
    attribute = get_article_attributes(article_id, "manuscript",
                                       COLUMN_HEADINGS["editor_middle_name"])[0]
    return attribute

@entities
def get_me_institution(article_id):
    attribute = get_article_attributes(article_id, "manuscript",
                                       COLUMN_HEADINGS["editor_institution"])[0]
    return attribute

@entities
def get_me_department(article_id):
    attribute = get_article_attributes(article_id, "manuscript",
                                       COLUMN_HEADINGS["editor_department"])[0]
    return attribute

@entities
def get_me_country(article_id):
    attribute = get_article_attributes(article_id, "manuscript",
                                       COLUMN_HEADINGS["editor_country"])[0]
    return attribute

def get_ethics(article_id):
    """
    needs a bit of refinement owing to serilaising of data by EJP
    """
    attribute = get_article_attributes(article_id, "manuscript",
                                       COLUMN_HEADINGS["ethics"])[0]

    return attribute

# authors table
def get_author_ids(article_id):
    author_ids = get_article_attributes(article_id, "authors",
                                        COLUMN_HEADINGS["author_id"])
    return author_ids

def get_author_attribute(article_id, author_id, attribute_name):
    article_author_index = index_authors_on_author_id()
    data_row = article_author_index[article_id][author_id]
    col_names = get_xls_col_names("authors")
    attribute = get_cell_value(attribute_name, col_names, data_row)
    return attribute

def get_author_position(article_id, author_id):
    attribute = get_author_attribute(article_id, author_id,
                                     COLUMN_HEADINGS["author_position"])
    return attribute

def get_author_email(article_id, author_id):
    attribute = get_author_attribute(article_id, author_id,
                                     COLUMN_HEADINGS["email"])
    return attribute

def get_author_contrib_type(article_id, author_id):
    attribute = get_author_attribute(article_id, author_id,
                                     COLUMN_HEADINGS["author_type"])
    return attribute

def get_author_dual_corresponding(article_id, author_id):
    attribute = get_author_attribute(article_id, author_id,
                                     COLUMN_HEADINGS["dual_corresponding"])
    return attribute

@entities
def get_author_last_name(article_id, author_id):
    attribute = get_author_attribute(article_id, author_id,
                                     COLUMN_HEADINGS["author_last_name"])
    return attribute

@entities
def get_author_first_name(article_id, author_id):
    attribute = get_author_attribute(article_id, author_id,
                                     COLUMN_HEADINGS["author_first_name"])
    return attribute

@entities
def get_author_middle_name(article_id, author_id):
    attribute = get_author_attribute(article_id, author_id,
                                     COLUMN_HEADINGS["author_middle_name"])
    return attribute

@entities
def get_author_institution(article_id, author_id):
    attribute = get_author_attribute(article_id, author_id,
                                     COLUMN_HEADINGS["author_institution"])
    return attribute

@entities
def get_author_department(article_id, author_id):
    attribute = get_author_attribute(article_id, author_id,
                                     COLUMN_HEADINGS["author_department"])
    return attribute

@entities
def get_author_city(article_id, author_id):
    attribute = get_author_attribute(article_id, author_id,
                                     COLUMN_HEADINGS["author_city"])
    return attribute

@entities
def get_author_country(article_id, author_id):
    attribute = get_author_attribute(article_id, author_id,
                                     COLUMN_HEADINGS["author_country"])
    return attribute

def get_author_state(article_id, author_id):
    attribute = get_author_attribute(article_id, author_id,
                                     COLUMN_HEADINGS["author_state"])
    return attribute

def get_author_conflict(article_id, author_id):
    attribute = get_author_attribute(article_id, author_id,
                                     COLUMN_HEADINGS["author_conflict"])
    return attribute

def get_author_orcid(article_id, author_id):
    attribute = get_author_attribute(article_id, author_id,
                                     COLUMN_HEADINGS["orcid"])
    return attribute

def get_group_authors(article_id):
    # Wrap in an exception because some empty rows throws IndexError
    try:
        attribute = get_article_attributes(article_id, "group_authors",
                                           COLUMN_HEADINGS["group_author"])[0]
    except IndexError:
        attribute = None
    return attribute

def get_datasets(article_id):
    try:
        attribute = get_article_attributes(article_id, "datasets",
                                           COLUMN_HEADINGS["datasets"])[0]
    except IndexError:
        attribute = None
    return attribute

# funding
@memoize
def index_funding_table():
    """
    Rows in the funding CSV are to be uniquely identified by three column values
    article_id + author_id + funder_position
    This will return a three dimensional dict with those hierarchies
    """
    table_type = "funding"

    logger.info("in index_funding_table")
    path = get_xls_path(table_type)

    # get the data and the row of colnames
    data_rows = get_xls_data_rows(table_type)
    col_names = get_xls_col_names(table_type)

    # logger.info("data_rows: " + str(data_rows))
    logger.info("col_names: " + str(col_names))

    article_index = {}
    for data_row in data_rows:
        article_id = get_cell_value('poa_m_ms_no', col_names, data_row)
        author_id = get_cell_value(COLUMN_HEADINGS["author_id"], col_names, data_row)
        funder_position = get_cell_value(COLUMN_HEADINGS["funder_position"], col_names, data_row)

        # Crude multidimentional dict builder
        if article_id not in article_index:
            article_index[article_id] = {}
        if author_id not in article_index[article_id]:
            article_index[article_id][author_id] = {}

        article_index[article_id][author_id][funder_position] = data_row

    #print article_index
    return article_index

def get_funding_ids(article_id):
    """
    Return funding table keys as a list of tuples
    for a particular article_id
    """
    funding_ids = []

    for key, value in index_funding_table().iteritems():
        if key == article_id:
            for key_2, value_2 in value.iteritems():
                for key_3, value_3 in value_2.iteritems():
                    funding_ids.append((key, key_2, key_3))

    return funding_ids

def get_funding_attribute(article_id, author_id, funder_position, attribute_name):
    funding_article_index = index_funding_table()

    data_row = funding_article_index[str(article_id)][str(author_id)][str(funder_position)]

    col_names = get_xls_col_names("funding")
    attribute = get_cell_value(attribute_name, col_names, data_row)
    return attribute

def get_funder(article_id, author_id, funder_position):
    attribute = get_funding_attribute(article_id, author_id, funder_position,
                                     COLUMN_HEADINGS["funder"])
    return attribute

def get_award_id(article_id, author_id, funder_position):
    attribute = get_funding_attribute(article_id, author_id, funder_position,
                                     COLUMN_HEADINGS["award_id"])
    return attribute

def get_funder_identifier(article_id, author_id, funder_position):
    attribute = get_funding_attribute(article_id, author_id, funder_position,
                                     COLUMN_HEADINGS["funder_identifier"])
    return attribute

def get_funding_note(article_id):
    attribute = get_article_attributes(article_id, "manuscript",
                                       COLUMN_HEADINGS["funding_note"])[0]
    return attribute

## conversion functions
def get_elife_doi(article_id):
    """
    Given an article_id, return a DOI for the eLife journal
    """
    doi = "10.7554/eLife." + str(int(article_id)).zfill(5)
    return doi

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
        try:
            char_list = re.findall("[A-Z]|\-", str(middle_name))
        except UnicodeEncodeError:
            # Regular expression failed on unicode characters,
            # failover by using the first character
            char_list = []
            char_list.append(middle_name[0])
        initials = "".join(char_list)

    if initials == "":
        return None
    return initials

def unserialise_angle_brackets(escaped_string):
    unserial_xml = escaped_string.replace(settings.LESS_THAN_ESCAPE_SEQUENCE, "<")
    unserial_xml = unserial_xml.replace(settings.GREATER_THAN_ESCAPE_SEQUENCE, ">")
    return unserial_xml

def decode_cp1252(str):
    """
    CSV files look to be in CP-1252 encoding (Western Europe)
    Decoding to ASCII is normally fine, except when it gets an O umlaut, for example
    In this case, values must be decoded from cp1252 in order to be added as unicode
    to the final XML output.
    This function helps do that in selected places, like on author surnames
    """
    try:
        # See if it is not safe to encode to ascii first
        junk = str.encode('ascii')
    except (UnicodeEncodeError, UnicodeDecodeError):
        # Wrap the decode in another exception to make sure this never fails
        try:
            str = str.decode('cp1252')
        except:
            pass
    return str

def parse_ethics(ethic):
    """
    Given angle bracket escaped XML string, parse
    animal and human ethic comments, and return
    a list of strings if involved_comments tag
    is found. Boiler plate prefix added too.
    """

    ethics = []

    # Decode escaped angle brackets
    logger.info("ethic is " + str(ethic))
    ethic_xml = unserialise_angle_brackets(ethic)
    logger.info("ethic is " + str(ethic_xml))

    # Parse XML
    encoding = 'utf-8'
    reparsed = minidom.parseString(ethic_xml)

    # Extract comments
    for ethic_type in 'animal_subjects', 'human_subjects':
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

def parse_datasets(datasets_content):
    """
    Datasets content is XML with escaped angle brackets
    """
    datasets = []

    # Decode escaped angle brackets
    logger.info("datasets is " + str(datasets_content))
    datasets_xml = unserialise_angle_brackets(datasets_content)
    logger.info("datasets is " + str(datasets_xml))

    # Parse XML
    encoding = 'utf-8'
    reparsed = minidom.parseString(datasets_xml)

    # Extract comments
    for dataset_type in 'datasets', 'prev_published_datasets':
        datasets_nodes = reparsed.getElementsByTagName(dataset_type)[0]

        for d_nodes in datasets_nodes.getElementsByTagName("dataset"):
            dataset = eLifeDataset()

            dataset.dataset_type = dataset_type

            for node in d_nodes.childNodes:

                if node.nodeName == 'authors_text_list' and len(node.childNodes) > 0:
                    text_node = node.childNodes[0]
                    for author_name in text_node.nodeValue.split(','):
                        dataset.add_author(author_name.lstrip())

                if node.nodeName == 'title':
                    text_node = node.childNodes[0]
                    dataset.title = entity_to_unicode(text_node.nodeValue)

                if node.nodeName == 'id':
                    text_node = node.childNodes[0]
                    dataset.source_id = entity_to_unicode(text_node.nodeValue)

                if node.nodeName == 'license_info':
                    text_node = node.childNodes[0]
                    dataset.license_info = entity_to_unicode(text_node.nodeValue)

                if node.nodeName == 'year' and len(node.childNodes) > 0:
                    text_node = node.childNodes[0]
                    dataset.year = entity_to_unicode(text_node.nodeValue)

            datasets.append(dataset)

    return datasets

def parse_group_authors(group_authors):
    """
    Given a raw group author value from the data files,
    check for empty, whitespace, zero
    If not empty, remove extra numbers from the end of the string
    Return a dictionary of dict[author_position] = collab_name
    """
    group_author_dict = {}
    if group_authors.strip() == "":
        group_author_dict = None
    elif group_authors.strip() == "0":
        group_author_dict = None
    else:

        # Parse out elements into a list, clean and
        #  add the the dictionary using some steps

        # Split the string on the first delimiter
        group_author_list = group_authors.split('order_start')

        for group_author_string in group_author_list:
            if group_author_string == "":
                continue

            # Now split on the second delimiter
            position_and_name = group_author_string.split('order_end')

            author_position = position_and_name[0]

            # Strip numbers at the end
            group_author = position_and_name[1].rstrip("1234567890")

            # Finally, add to the dict noting the authors position
            group_author_dict[author_position] = group_author

    return group_author_dict

if __name__ == "__main__":

    test_article_id = "12717"

    logger.info("about to start the test program")
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

    funder_ids = get_funding_ids(test_article_id)
    for (article_id, author_id, funder_position) in funder_ids:
        funder_identifier = get_funder_identifier(article_id, author_id, funder_position)
        funder = get_funder(article_id, author_id, funder_position)
        award_id = get_award_id(article_id, author_id, funder_position)
        print ", ".join([funder_position, funder_identifier, funder, award_id])


