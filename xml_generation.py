from generatePoaXml import *
from parseCSVFiles import *
import xlrd
import settings as settings
import logging
import os

"""
read from an xls file
output an xml file

# Gotchas
TODO: currnet XLS does not provide author contrib type TODO: query for author contrib type
TODO: we need a decision on what we do with middle names, for now we are ignoring them
TODO: print out authors in their contrib order
TODO: add contrib-type
TODO: add managing editor information
TODO: add subjects

"""

logger = logging.getLogger('xml_gen')
hdlr = logging.FileHandler('xml_gen.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

# set output directory
TARGET_OUTPUT_DIR = settings.TARGET_OUTPUT_DIR

def instantiate_article(article_id):
	logger.info("in instantiate_article for " + str(article_id))
	try:
		doi = get_doi(article_id)
		# Fallback if doi string is blank, default to eLife concatenated
		if doi.strip() == "":
			doi = get_elife_doi(article_id)
		#title = get_title(article_id)
		article = eLifePOA(doi, title=None)
		return article
	except:
		logger.error("could not create article class")

def set_title(article, article_id):
	logger.info("in set_title")
	#try:
	title = get_title(article_id)
	article.title = convert_to_xml_string(title)
	return True
	#except:
	#	logger.error("could not set title ")
	#	return False

def set_abstract(article, article_id):
	logger.info("in set_abstract")
	try:
		abstract = get_abstract(article_id)
		article.abstract = convert_to_xml_string(abstract)
		article.manuscript = article_id
		return True
	except:
		logger.error("could not set abstract ")
		return False

def set_articleType(article, article_id):
	logger.info("in set_articleType")
	try:
		articleType_id = get_articleType(article_id)
		
		# Boilerplate article-type values based on id in CSV file
		article_type_index = {}
		
		article_type_index['1']  = {
			'article_type':    'research-article',
			'display_channel': 'Research article'}
		article_type_index['10'] = {
			'article_type':    'research-article',
			'display_channel': 'Feature article'}
		article_type_index['14'] = {
			'article_type':    'research-article',
			'display_channel': 'Short report'}
		
		article_type = article_type_index[str(articleType_id)]
		article.articleType = article_type['article_type']
		article.display_channel = article_type['display_channel']
		return True
	except:
		logger.error("could not set articleType")
		return False

def set_license(article, article_id):
	logger.info("in set_license")
	try:
		license_id = get_license(article_id)
		license = eLifeLicense(license_id)
		article.license = license
		return True
	except:
		logger.error("could not set license")
		return False

def set_dates(article, article_id):
	logger.info("in set_dates")
	try:
		accepted_date = get_accepted_date(article_id)
		t_accepted = time.strptime(accepted_date.split()[0], "%Y-%m-%d")
		accepted = eLifeDate("accepted", t_accepted)
		article.add_date(accepted)
		logger.info(str(accepted_date))
		
		received_date = get_received_date(article_id)
		t_received = time.strptime(received_date.split()[0], "%Y-%m-%d")
		received = eLifeDate("received", t_received)
		article.add_date(received)

		# set the license date to be the same as the accepted date
		date_license = eLifeDate("license", t_accepted)
		article.add_date(date_license)
		return True
	except:
		logger.error("could not set dates")
		return False

def set_ethics(article, article_id):
	logger.info("in set_ethics")
	try:
		ethic = get_ethics(article_id)
		logger.info(ethic)
		if ethic:
			ethics = parse_ethics(ethic)
			for e in ethics:
				article.add_ethic(e)
		return True
	except:
		# logger.error("could not set ethics")
		return False

def set_categories(article, article_id):
	logger.info("in set_categories")
	try:
		categories = get_subjects(article_id)
		for category in categories:
			article.add_article_category(category)
		return True
	except:
		logger.error("could not set categories")
		return False

def set_organsims(article, article_id):
	logger.info("in set_categories")
	try:
		research_organisms = get_organisms(article_id)
		for research_organism in research_organisms:
			article.add_research_organism(research_organism)
		return True
	except:
		logger.error("could not set organisms")
		return False

def set_author_info(article, article_id):
	# author information
	logger.info("in set_author_info")
	try:
		author_ids = get_author_ids(article_id)
		for author_id in author_ids:

			author_type = "author"

			first_name = get_author_first_name(article_id, author_id)
			last_name = get_author_last_name(article_id, author_id)
			middle_name = get_author_middle_name(article_id, author_id)
			initials = middle_name_initials(middle_name)
			if initials:
				# Middle initials
				first_name += " " + initials
			author = eLifePOSContributor(author_type, last_name, first_name)
			affiliation = ContributorAffiliation()

			department = get_author_department(article_id, author_id)
			if department.strip() != "":
				affiliation.department = department
			affiliation.institution = get_author_institution(article_id, author_id)
			city = get_author_city(article_id, author_id)
			if city.strip() != "":
				affiliation.city = city
			affiliation.country = get_author_country(article_id, author_id)

			contrib_type = get_author_contrib_type(article_id, author_id)
			dual_corresponding = get_author_dual_corresponding(article_id, author_id)
			if contrib_type == "Corresponding Author" or dual_corresponding == 1:
				email = get_author_email(article_id, author_id)
				affiliation.email = get_author_email(article_id, author_id)
				author.corresp = True

			conflict = get_author_conflict(article_id, author_id)
			if conflict.strip() != "":
				author.set_conflict(conflict)

			author.auth_id = `int(author_id)`
			author.set_affiliation(affiliation)
			article.add_contributor(author)
		return True
	except:
		logger.error("could not set authors")
		return False

def set_editor_info(article, article_id):
	logger.info("in set_editor_info")
	try:
		author_type = "editor"

		first_name = get_me_first_nm(article_id)
		last_name = get_me_last_nm(article_id)
		middle_name = get_me_middle_nm(article_id)
		initials = middle_name_initials(middle_name)
		if initials:
			# Middle initials
			first_name += " " + initials
		editor = eLifePOSContributor(author_type, last_name, first_name)  # creates an instance of the POSContributor class
		logger.info("editor is: " + str(editor))
		logger.info("getting ed id for article " + str(article_id))
		logger.info("editor id is " + str(get_me_id(article_id)))
		logger.info(str(type(get_me_id(article_id))))
		editor.auth_id = `int(get_me_id(article_id))`
		affiliation = ContributorAffiliation()
		department =  get_me_department(article_id)
		if department.strip() != "":
			affiliation.department = department
		affiliation.institution = get_me_institution(article_id)
		affiliation.country = get_me_country(article_id)

		# editor.auth_id = `int(author_id)`we have a me_id, but I need to determine whether that Id is the same as the relevent author id
		editor.set_affiliation(affiliation)
		article.add_contributor(editor)
		return True
	except:
		logger.error("could not set editor")
		return False

def write_xml(article_id, xml, dir = ''):
	f = open(dir + os.sep + 'elife_poa_e' + str(int(article_id)).zfill(5) + '.xml', "wb")
	f.write(xml.prettyXML())
	f.close()

def build_xml_for_article(article_id):
	error_count = 0
	
	# Only happy with string article_id - cast it now to be safe!
	article_id = str(article_id)
	
	article = instantiate_article(article_id)
	if not set_title(article, article_id): error_count = error_count + 1
	if not set_abstract(article, article_id): error_count = error_count + 1
	if not set_articleType(article, article_id): error_count = error_count + 1
	if not set_license(article, article_id): error_count = error_count + 1
	if not set_dates(article, article_id): error_count = error_count + 1
	if not set_ethics(article, article_id): error_count = error_count + 1
	if not set_categories(article, article_id): error_count = error_count + 1
	if not set_organsims(article, article_id): error_count = error_count + 1
	if not set_author_info(article, article_id): error_count = error_count + 1
	if not set_editor_info(article, article_id): error_count = error_count + 1

	print error_count

	# default conflict text
	article.conflict_default = "The authors declare that no competing interests exist."

	if error_count == 0:
		try:
			article_xml = eLife2XML(article)
			logger.info("generated xml for " + str(article_id))
			write_xml(article_id, article_xml, dir = TARGET_OUTPUT_DIR)
			logger.info("xml written for " + str(article_id))
			print "written " + article_id
			return True
		except:
			logger.error("could not generate or write xml for " + str(article_id))
			return False
	else:
		logger.warning("the following article did not have enough components and xml was not generated " + str(article_id))
		logger.warning("warning count was " + str(error_count))
		return False

@memoize
def index_manuscripts_on_article_id():
	return index_table_on_article_id("manuscript")

if __name__ == "__main__":
	# get a list of active article numbers
	#article_ids = index_authors_on_article_id().keys()
	article_ids = index_manuscripts_on_article_id().keys()
	TARGET_OUTPUT_DIR = settings.TARGET_OUTPUT_DIR

	for article_id in article_ids:
		print "working on ", article_id
		xml = build_xml_for_article(article_id)
		logging.info("")
		logging.error("")
