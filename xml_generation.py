from generatePoaXml import *
from parseXlsFiles import * 
import xlrd


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

def build_xml_for_article(article_id):
	doi = get_doi(article_id)
	title = get_title(article_id)
	#uri = doi2uri(doi)
	article = eLifePOA(doi, title)
	#
	abstract = get_abstract(article_id)
	article.abstract = abstract
	article.manuscript = article_id
	#
	license_id = get_license(article_id)
	license = eLifeLicense(license_id)
	article.license = license
	#
	accepted_date = get_accepted_date(article_id)

	t_accepted = time.strptime(accepted_date.split()[0], "%Y-%m-%d")
	accepted = eLifeDate("accepted", t_accepted)
	article.add_date(accepted)
	# Use accepted date as the received date
	received = eLifeDate("received", t_accepted)
	article.add_date(received)
	#
	# set the license date to be the same as the accepted date
	date_license = eLifeDate("license", t_accepted)
	article.add_date(date_license)

	# default conflict text
	article.conflict_default = "The authors declare that no competing interests exist."

	# ethics
	ethic = get_ethics(article_id)
	if ethic:
		article.add_ethic(ethic)

	# categories
	categories = get_subjects(article_id)
	for category in categories:
		article.add_article_category(category)

	# research organism
	research_organisms = get_organisms(article_id)
	for research_organism in research_organisms:
		article.add_research_organism(research_organism)

	# author information 
	author_ids = get_author_ids(article_id)
	for author_id in author_ids:

		author_type = "author"

		first_name = get_author_first_name(article_id, author_id)      
		last_name = get_author_last_name(article_id, author_id) 
		author = eLifePOSContributor(author_type, last_name, first_name)
		affiliation = ContributorAffiliation()

		affiliation.department = get_author_department(article_id, author_id)
		affiliation.institution = get_author_institution(article_id, author_id)
		affiliation.city = get_author_city(article_id, author_id)
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

	author_type = "editor"

	first_name = get_me_first_nm(article_id)
	last_name = get_me_last_nm(article_id)	

	editor = eLifePOSContributor(author_type, last_name, first_name)
	editor.auth_id = `int(get_me_id(article_id))`
	affiliation = ContributorAffiliation()
	affiliation.department = get_me_department(article_id)
	affiliation.institution = get_me_institution(article_id)
	affiliation.country = get_me_country(article_id)

	# editor.auth_id = `int(author_id)`we have a me_id, but I need to determine whether that Id is the same as the relevent author id
	editor.set_affiliation(affiliation)
	article.add_contributor(editor)

	article_xml = eLife2XML(article)
	return article_xml

def write_xml(article_id, xml, dir = ''):
	f = open(dir + 'elife_poa_e' + str(int(article_id)).zfill(5) + '.xml', "wb")
	f.write(xml.prettyXML())
	f.close()

if __name__ == "__main__":
	# get a list of active article numbers 
	article_ids = index_authors_on_article_id().keys()
	TARGET_OUTPUT_DIR = "generated_xml_output/"

	for article_id in article_ids:
		# xml = build_xml_for_article(article_id)

		try: 
			xml = build_xml_for_article(article_id)
			write_xml(article_id, xml, dir = TARGET_OUTPUT_DIR)
			print "xml built for ", article_id
			# print xml.prettyXML()
		except:
			print "xml build failed for", article_id
 