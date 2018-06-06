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
    try:
        title = get_title(article_id)
        article.title = convert_to_xml_string(title)
        return True
    except:
        logger.error("could not set title ")
        return False

def set_abstract(article, article_id):
    logger.info("in set_abstract")
    try:
        abstract = decode_cp1252(get_abstract(article_id))
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

        article_type_index['1'] = {
            'article_type':    'research-article',
            'display_channel': 'Research Article'}
        article_type_index['10'] = {
            'article_type':    'research-article',
            'display_channel': 'Feature Article'}
        article_type_index['14'] = {
            'article_type':    'research-article',
            'display_channel': 'Short Report'}
        article_type_index['15'] = {
            'article_type':    'research-article',
            'display_channel': 'Research Advance'}
        article_type_index['19'] = {
            'article_type':    'research-article',
            'display_channel': 'Tools and Resources'}

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
        if received_date.strip() == "":
            # Use the alternate date column receipt_date if received_date is blank
            received_date = get_receipt_date(article_id)
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


def set_datasets(article, article_id):
    logger.info("in set_datasets")
    try:
        datasets = get_datasets(article_id)
        logger.info(datasets)
        if datasets:
            dataset_objects, data_availability = parse_datasets(datasets)
            for dataset in dataset_objects:
                article.add_dataset(dataset)
            if data_availability:
                article.data_availability = convert_to_xml_string(data_availability)
        return True
    except:
        logger.error("could not set datasets")
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
            if research_organism.strip() != "":
                article.add_research_organism(research_organism)
        return True
    except:
        logger.error("could not set organisms")
        return False

def set_keywords(article, article_id):
    logger.info("in set_keywords")
    try:
        keywords = get_keywords(article_id)
        for keyword in keywords:
            article.add_author_keyword(keyword)
        return True
    except:
        logger.error("could not set keywords")
        return False

def set_author_info(article, article_id):
    """
    author information
    Save the contributor and their position in the list in a dict,
    for both authors and group authors,
    Then add the contributors to the article object in order of their position
    """
    logger.info("in set_author_info")
    authors_dict = {}
    try:
        author_ids = get_author_ids(article_id)
        for author_id in author_ids:

            author_type = "author"

            first_name = decode_cp1252(get_author_first_name(article_id, author_id))
            last_name = decode_cp1252(get_author_last_name(article_id, author_id))
            middle_name = decode_cp1252(get_author_middle_name(article_id, author_id))
            #initials = middle_name_initials(middle_name)
            if middle_name.strip() != "":
                # Middle name add to the first name / given name
                first_name += " " + middle_name
            author = eLifePOSContributor(author_type, last_name, first_name)
            affiliation = ContributorAffiliation()

            department = decode_cp1252(get_author_department(article_id, author_id))
            if department.strip() != "":
                affiliation.department = department
            affiliation.institution = decode_cp1252(get_author_institution(article_id, author_id))
            city = decode_cp1252(get_author_city(article_id, author_id))
            if city.strip() != "":
                affiliation.city = city
            affiliation.country = get_author_country(article_id, author_id)

            contrib_type = get_author_contrib_type(article_id, author_id)
            dual_corresponding = get_author_dual_corresponding(article_id, author_id)
            if (contrib_type == "Corresponding Author" or
                    (dual_corresponding.strip() != '' and int(dual_corresponding.strip()) == 1)):
                email = get_author_email(article_id, author_id)
                affiliation.email = get_author_email(article_id, author_id)
                author.corresp = True

            conflict = get_author_conflict(article_id, author_id)
            if conflict.strip() != "":
                author.set_conflict(conflict)

            orcid = get_author_orcid(article_id, author_id)
            if orcid.strip() != "":
                author.orcid = orcid

            author.auth_id = `int(author_id)`
            author.set_affiliation(affiliation)

            author_position = get_author_position(article_id, author_id)
            # Add the author to the dictionary recording their position in the list
            authors_dict[int(author_position)] = author

        # Add group author collab contributors, if present
        group_authors = get_group_authors(article_id)
        if group_authors:
            # Parse the group authors string
            group_author_dict = parse_group_authors(group_authors)

            if group_author_dict:
                for author_position, collab_name in (
                    sorted(group_author_dict.items(), key=group_author_dict.get)):

                    author_type = "author"
                    last_name = None
                    first_name = None
                    collab = collab_name
                    author = eLifePOSContributor(author_type, last_name, first_name, collab)

                    # Add the author to the dictionary recording their position in the list
                    authors_dict[int(author_position)] = author

        # Finally add authors to the article sorted by their position
        for author_position, author in sorted(authors_dict.items(), key=authors_dict.get):
            #print article_id, author_position, author
            article.add_contributor(author)

        return True
    except:
        logger.error("could not set authors")
        return False

def set_editor_info(article, article_id):
    logger.info("in set_editor_info")
    try:
        author_type = "editor"

        first_name = decode_cp1252(get_me_first_nm(article_id))
        last_name = decode_cp1252(get_me_last_nm(article_id))
        middle_name = decode_cp1252(get_me_middle_nm(article_id))
        #initials = middle_name_initials(middle_name)
        if middle_name.strip() != "":
            # Middle name add to the first name / given name
            first_name += " " + middle_name
        # create an instance of the POSContributor class
        editor = eLifePOSContributor(author_type, last_name, first_name)
        logger.info("editor is: " + str(editor))
        logger.info("getting ed id for article " + str(article_id))
        logger.info("editor id is " + str(get_me_id(article_id)))
        logger.info(str(type(get_me_id(article_id))))
        editor.auth_id = `int(get_me_id(article_id))`
        affiliation = ContributorAffiliation()
        department = get_me_department(article_id)
        if department.strip() != "":
            affiliation.department = department
        affiliation.institution = get_me_institution(article_id)
        affiliation.country = get_me_country(article_id)

        # editor.auth_id = `int(author_id)`we have a me_id, but I need to determine
        # whether that Id is the same as the relevent author id
        editor.set_affiliation(affiliation)
        article.add_contributor(editor)
        return True
    except:
        logger.error("could not set editor")
        return False

def set_funding(article, article_id):
    """
    Instantiate one eLifeFundingAward for each funding award
    Add principal award recipients in the order of author position for the article
    Finally add the funding objects to the article in the order of funding position
    """
    logger.info("in set_funding")
    try:
        # Set the funding note from the manuscript level
        article.funding_note = get_funding_note(article_id)

        # Query for all funding award data keys
        funder_ids = get_funding_ids(article_id)

        # Keep track of funding awards by position in a dict
        funding_awards = {}

        # First pass, build the funding awards
        for (article_id, author_id, funder_position) in funder_ids:
            #print (article_id, author_id, funder_position)
            funder_identifier = get_funder_identifier(article_id, author_id, funder_position)
            funder = decode_cp1252(clean_funder(get_funder(article_id, author_id, funder_position)))
            award_id = get_award_id(article_id, author_id, funder_position)

            if funder_position not in funding_awards.keys():
                # Initialise the object values
                funding_awards[funder_position] = eLifeFundingAward()
                if funder:
                    funding_awards[funder_position].institution_name = funder
                if funder_identifier and funder_identifier.strip() != "":
                    funding_awards[funder_position].institution_id = funder_identifier
                if award_id and award_id.strip() != "":
                    funding_awards[funder_position].add_award_id(award_id)

        # Second pass, add the primary award recipients in article author order
        for position, award in funding_awards.iteritems():
            for contrib in article.contributors:
                for (article_id, author_id, funder_position) in funder_ids:
                    if position == funder_position and contrib.auth_id == author_id:
                        funding_awards[position].add_principal_award_recipient(contrib)

        # Add funding awards to the article object, sorted by position
        for position, award in sorted(funding_awards.iteritems()):
            article.add_funding_award(award)

        return True
    except:
        logger.error("could not set funding")
        return False

def write_xml(article_id, xml, dir=''):
    f = open(dir + os.sep + 'elife_poa_e' + str(int(article_id)).zfill(5) + '.xml', "wb")
    f.write(xml.prettyXML())
    f.close()

def build_article_for_article(article_id):
    """
    Given an article_id, instantiate and populate the eLifePOA article object
    Refactored for easier testing, but primarily used by build_xml_for_article
    """
    error_count = 0
    error_messages = []

    # Only happy with string article_id - cast it now to be safe!
    article_id = str(article_id)

    article = instantiate_article(article_id)

    # Run each of the below functions to build the article object components
    article_set_functions = [set_title, set_abstract, set_articleType, set_license,
                            set_dates, set_ethics, set_datasets, set_categories,
                            set_organsims, set_author_info, set_editor_info, set_keywords,
                            set_funding]
    for set_function in article_set_functions:
        if not set_function(article, article_id):
            error_count = error_count + 1
            error_messages.append("article_id " + str(article_id)
                                  + " error in " + set_function.__name__)

    # Building from CSV data it must be a POA type, set it
    if article:
        article.is_poa = True

    print error_count

    # default conflict text
    if article:
        article.conflict_default = "The authors declare that no competing interests exist."

    if error_count == 0:
        return article, error_count, error_messages
    else:
        return None, error_count, error_messages

def build_xml_for_article(article_id):
    article, error_count, error_messages = build_article_for_article(article_id)
    if article:
        return output_xml_for_article(article, article_id)
    else:
        logger.warning("the following article did not have enough components and " +
                       "xml was not generated " + str(article_id))
        logger.warning("warning count was " + str(error_count))
        if len(error_messages) > 0:
            logger.warning(", ".join(error_messages))
        return False

def output_xml_for_article(article, article_id):
    try:
        article_xml = eLife2XML(article)
        logger.info("generated xml for " + str(article_id))
        write_xml(article_id, article_xml, dir=settings.TARGET_OUTPUT_DIR)
        logger.info("xml written for " + str(article_id))
        print "written " + str(article_id)
        return True
    except:
        logger.error("could not generate or write xml for " + str(article_id))
        return False


@memoize
def index_manuscripts_on_article_id():
    return index_table_on_article_id("manuscript")

if __name__ == "__main__":
    # get a list of active article numbers
    #article_ids = index_authors_on_article_id().keys()
    article_ids = index_manuscripts_on_article_id().keys()
    article_ids = ['31018']
    for article_id in article_ids:
        print "working on ", article_id
        xml = build_xml_for_article(article_id)
        logging.info("")
        logging.error("")
