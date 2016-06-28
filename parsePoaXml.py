import os
from generatePoaXml import *
import settings
from elifetools import parseJATS as parser
from bs4 import BeautifulSoup

"""
Parse PoA XML file and can instantiate a eLifePOA object from the data
"""

def text_from_affiliation_elements(department, institution, city, country):
    """
    Given an author affiliation from
    """
    text = ""

    for element in (department, institution, city, country):
        if text != "":
            text += ", "

        if element:
            text += element

    return text

def build_contributors(authors, contrib_type):
    """
    Given a list of authors from the parser, instantiate contributors
    objects and build them
    """

    contributors = []

    for author in authors:
        contributor = None
        author_contrib_type = contrib_type

        surname = author.get("surname")
        given_name = author.get("given-names")
        collab = author.get("collab")

        # Small hack for on-behalf-of type when building authors
        #  use on-behalf-of as the contrib_type
        if author.get("type") and author.get("type") == "on-behalf-of":
            collab = author.get("on-behalf-of")
            author_contrib_type = "on-behalf-of"

        if surname or collab:
            contributor = eLifePOSContributor(author_contrib_type, surname, given_name, collab)
        else:
            continue

        contributor.group_author_key = author.get("group-author-key")
        contributor.orcid = author.get("orcid")
        if author.get("corresp"):
            contributor.corresp = True
        else:
            contributor.corresp = False

        # Affiliations, compile text for each
        department = []
        institution = []
        city = []
        country = []

        if author.get("affiliations"):
            for aff in author.get("affiliations"):
                department.append(aff.get("dept"))
                institution.append(aff.get("institution"))
                city.append(aff.get("city"))
                country.append(aff.get("country"))

        # Turn the set of lists into ContributorAffiliation
        for index in range(0, len(institution)):
            affiliation = ContributorAffiliation()
            affiliation.department = department[index]
            affiliation.institution = institution[index]
            affiliation.city = city[index]
            affiliation.country = country[index]

            affiliation.text = text_from_affiliation_elements(
                affiliation.department,
                affiliation.institution,
                affiliation.city,
                affiliation.country)

            contributor.set_affiliation(affiliation)

        # Finally add the contributor to the list
        if contributor:
            contributors.append(contributor)

    return contributors

def build_funding(award_groups):
    """
    Given a funding data, format it
    """
    if not award_groups:
        return []

    funding_awards = []

    for award_group in award_groups:
        for id, award_group in award_group.iteritems():
            award = eLifeFundingAward()

            if award_group.get('id-type') == "FundRef":
                award.institution_id = award_group.get('id')

            award.institution_name = award_group.get('institution')

            # TODO !!! Check for multiple award_id, if exists
            if award_group.get('award-id'):
                award.add_award_id(award_group.get('award-id'))

            funding_awards.append(award)

    return funding_awards


def build_ref_list(refs):
    """
    Given parsed references build a list of ref objects
    """
    ref_list = []

    for reference in refs:
        ref = eLifeRef()

        # Publcation Type
        if reference.get('publication-type'):
            ref.publication_type = reference.get('publication-type')

        # Article title
        if reference.get('article_title'):
            ref.article_title = reference.get('article_title')

        # Article title
        if reference.get('source'):
            ref.source = reference.get('source')

        # Volume
        if reference.get('volume'):
            ref.volume = reference.get('volume')

        # First page
        if reference.get('fpage'):
            ref.fpage = reference.get('fpage')

        # Last page
        if reference.get('lpage'):
            ref.lpage = reference.get('lpage')

        # DOI
        if reference.get('reference_id'):
            ref.doi = reference.get('reference_id')

        # Year
        if reference.get('year'):
            ref.year = reference.get('year')

        # elocation-id
        if reference.get('elocation-id'):
            ref.elocation_id = reference.get('elocation-id')

        # Authors
        if reference.get('authors'):
            for author in reference.get('authors'):
                # TODO - Need to parse surname and given-names
                ref_author = {}
                if 'surname' in author:
                    ref_author['surname'] = author['surname']
                    ref.add_author(ref_author)
                elif 'collab' in author:
                    ref_author['collab'] = author['collab']
                    ref.add_author(ref_author)

        ref_list.append(ref)

    return ref_list


def component_title(component):
    """
    Label, title and caption
    Title is the label text plus the title text
    Title may contain italic tag, etc.
    """

    title = u''

    label_text = u''
    title_text = u''
    if component.get('label'):
        label_text = component.get('label')

    if component.get('title'):
        title_text = component.get('title')

    title = unicode(label_text)
    if label_text != '' and title_text != '':
        title += ' '
    title += unicode(title_text)

    if component.get('type') == 'abstract' and title == '':
        title = 'Abstract'

    return title


def build_components(components):
    """
    Given parsed components build a list of component objects
    """
    component_list = []

    for comp in components:
        component = eLifeComponent()

        # DOI and Resource URL
        if comp.get('doi'):
            component.doi = comp.get('doi')
            # Based on lookup URL path logic
            doi_resource = "http://elifesciences.org/lookup/doi/" + comp.get('doi')
            component.doi_resource = doi_resource

        if component_title(comp) != '':
            component.title = component_title(comp)

        # Subtitle
        if comp.get('type') in ['supplementary-material', 'fig']:

            if comp.get('full_caption'):
                subtitle = comp.get('full_caption')
                subtitle = clean_abstract(subtitle)
                component.subtitle = subtitle

        # Mime type
        if comp.get('type') in ['abstract', 'table-wrap', 'sub-article',
                                'chem-struct-wrap', 'boxed-text']:
            component.mime_type = 'text/plain'
        if comp.get('type') in ['fig']:
            component.mime_type = 'image/tiff'
        elif comp.get('type') in ['media', 'supplementary-material']:
            if comp.get('mimetype') and comp.get('mime-subtype'):
                component.mime_type = (comp.get('mimetype') + '/'
                                       + comp.get('mime-subtype'))

        # Permissions
        component.permissions = comp.get('permissions')

        # Append it to our list of components
        component_list.append(component)

    return component_list



def build_related_articles(related_articles):
    """
    Given parsed data build a list of related article objects
    """
    article_list = []

    for related_article in related_articles:
        article = eLifeRelatedArticle()
        if related_article.get('xlink_href'):
            article.xlink_href = related_article.get('xlink_href')
        if related_article.get('related_article_type'):
            article.related_article_type = related_article.get('related_article_type')
        if related_article.get('ext_link_type'):
            article.ext_link_type = related_article.get('ext_link_type')

        # Append it to our list
        article_list.append(article)

    return article_list

def remove_tag(tag_name, string):

    """
    Remove unwanted tags from the string, keeping the contents it surrounds,
    parsing it as HTML, then only keep the body paragraph contents
    tag_name if ending in * can match tags starting with a value,
    e.g. mml:*   will remove any tag with name starting with mml:
    """
    if string is None:
        return None

    soup = BeautifulSoup(string)

    tags = soup.find_all(True)
    for tag in tags:
        if tag_name.endswith('*'):
            # Wildcard match capability
            if tag.name.startswith(tag_name[0:-1]):
                tag.unwrap()
        else:
            # Exact match
            if tag.name == tag_name:
                tag.unwrap()

    # If the abstract starts with a tag, and has only one p tag
    #   then it will not be enclosed in a p tag
    if hasattr(soup.body.p, "children") and len(soup.find_all('p')) == 1:
        return "".join(map(unicode, soup.body.p.children)) or None
    if hasattr(soup.body, "children"):
        # No p tag or more than one p tag, use all the children
        return "".join(map(unicode, soup.body.children)) or None
    else:
        return None

def clean_abstract(abstract):
    """
    Remove unwanted tags from abstract string,
    parsing it as HTML, then only keep the body paragraph contents
    """

    remove_tags = ['xref', 'ext-link', 'inline-formula', 'mml:*']
    for tag_name in remove_tags:
        abstract = remove_tag(tag_name, abstract)

    return abstract


def build_article_from_xml(article_xml_filename, detail="brief"):
    """
    Parse JATS XML with elifetools parser, and populate an
    eLifePOA article object
    Basic data crossref needs: article_id, doi, title, contributors with names set
    detail="brief" is normally enough,
    detail="full" will populate all the contributor affiliations that are linked by xref tags
    """

    error_count = 0

    soup = parser.parse_document(article_xml_filename)

    # Get DOI
    doi = parser.doi(soup)

    # Create the article object
    article = eLifePOA(doi, title=None)

    # Related articles
    article.related_articles = build_related_articles(parser.related_article(soup))

    # Get publisher_id and set object manuscript value
    publisher_id = parser.publisher_id(soup)
    article.manuscript = publisher_id

    # Set the articleType
    article_type = parser.article_type(soup)
    if article_type:
        article.articleType = article_type

    # title
    article.title = parser.full_title(soup)
    #print article.title

    # abstract
    article.abstract = clean_abstract(parser.full_abstract(soup))

    # digest
    article.digest = clean_abstract(parser.full_digest(soup))

    # elocation-id
    article.elocation_id = parser.elocation_id(soup)

    # contributors
    all_contributors = parser.contributors(soup, detail)
    author_contributors = filter(lambda con: con.get('type')
                                 in ['author', 'on-behalf-of'], all_contributors)
    contrib_type = "author"
    contributors = build_contributors(author_contributors, contrib_type)

    contrib_type = "author non-byline"
    authors = parser.authors(soup, contrib_type, detail)
    contributors_non_byline = build_contributors(authors, contrib_type)
    article.contributors = contributors + contributors_non_byline

    # license href
    license = eLifeLicense()
    license.href = parser.license_url(soup)
    article.license = license

    # article_category
    article.article_categories = parser.category(soup)

    # keywords
    article.author_keywords = parser.keywords(soup)

    # research organisms
    article.research_organisms = parser.research_organism(soup)

    # funding awards
    article.funding_awards = build_funding(parser.full_award_groups(soup))

    # references or citations
    article.ref_list = build_ref_list(parser.refs(soup))

    # components with component DOI
    article.component_list = build_components(parser.components(soup))

    # History dates
    date_types = ["received", "accepted"]
    for date_type in date_types:
        history_date = parser.history_date(soup, date_type)
        if history_date:
            date_instance = eLifeDate(date_type, history_date)
            article.add_date(date_instance)

    # Pub date
    pub_date = parser.pub_date(soup)
    if pub_date:
        date_instance = eLifeDate("pub", pub_date)
        article.add_date(date_instance)

    # Set the volume if present
    volume = parser.volume(soup)
    if volume:
        article.volume = volume

    article.is_poa = parser.is_poa(soup)

    return article, error_count


def build_articles_from_article_xmls(article_xmls):
    """
    Given a list of article XML filenames, convert to article objects
    """

    poa_articles = []
    detail = "full"

    for article_xml in article_xmls:
        print "working on ", article_xml
        article, error_count = build_article_from_xml(article_xml, detail)
        if error_count == 0:
            poa_articles.append(article)

    return poa_articles

if __name__ == '__main__':

    article_xlms = [#"elife_poa_e02935.xml"
                    #,"Feature.xml"
                    "elife_poa_e02923.xml"
                    , "elife00003.xml"
                    , "elife02676.xml"
                    ]
    poa_articles = []

    for article_xml in article_xlms:
        print "working on ", article_xml
        article, error_count = build_article_from_xml("generated_xml_output" +
                                                     os.sep + article_xml, detail="full")

        if error_count == 0:
            poa_articles.append(article)
        print article.doi




