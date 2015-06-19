import xml
import time
import datetime
import calendar
import re
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
        
        surname = author.get("surname")
        given_name = author.get("given_names")
        collab = author.get("collab")

        if surname or collab:
            contributor = eLifePOSContributor(contrib_type, surname, given_name, collab)
        else:
            continue
        
        contributor.group_author_key = author.get("group_author_key")
        contributor.orcid = author.get("orcid")
        if author.get("corresponding"):
            contributor.corresp = True
        else:
            contributor.corresp = False
            
        # Affiliations, compile text for each
        department = []
        institution = []
        city = []
        country = []
        
        if type(author.get("institution")) == list:
            for index in range(0, len(author.get("institution"))):
                department.append(author.get("department")[index])
                institution.append(author.get("institution")[index])
                city.append(author.get("city")[index])
                country.append(author.get("country")[index])
        else:
            department.append(author.get("department"))
            institution.append(author.get("institution"))
            city.append(author.get("city"))
            country.append(author.get("country"))
        
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
    
    funding_awards = []

    for id, award_group in award_groups.iteritems():
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
        if reference.get('publication_type'):
            ref.publication_type = reference.get('publication_type')
    
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
        # TODO!!!

        # Year
        if reference.get('year'):
            ref.year = reference.get('year')
            
        # Authors
        if reference.get('authors'):
            for author in reference.get('authors'):
                # TODO - Need to parse surname and given-names
                ref_author = {}
                if 'surname' in author:
                    ref_author['surname'] = author['surname']
                    ref.add_author(ref_author)

        ref_list.append(ref)

    return ref_list



def build_components(components):
    """
    Given parsed components build a list of component objects
    """
    component_list = []
    
    for comp in components:
        component = eLifeComponent()
        
        if comp.get('doi'):
            component.doi = comp.get('doi')
        
        # Depending on the type of parent tag, extract different content
        if comp.get('type') == 'table-wrap':
            # TODO!!!
            pass
        elif comp.get('type') == 'supplementary-material':
            # TODO!!!
            pass   
        elif comp.get('type') == 'fig':
            # Figures
            
            # Title is the label text plus the title text
            # Title may contain italic tag, etc.
            label_text = u''
            title_text = u''
            
            if comp.get('label'):
                label_text = comp.get('label')
                
            if comp.get('title'):
                title_text = comp.get('title')

            component.title = unicode(label_text) + ' ' + unicode(title_text)
                
            if comp.get('full_caption'):
                subtitle = comp.get('full_caption')
                subtitle = clean_abstract(subtitle)
                component.subtitle = subtitle
            
            # Mime type
            # TODO!!
            """
            for graphic_tag in parent_tag.findall('./graphic'):
                # There is a graphic tag, set as tiff
                component.mime_type = 'image/tiff'
            """
            """
            for media_tag in parent_tag.findall('./media'):
                # There is a media tag i.e. video
                # TODO!!!
            """
        
        # Resource URL
        if comp.get('doi'):
            # TO DO - Base it on prevailing URL path logic
            doi_resource = "http://elifesciences.org/lookup/doi/" + comp.get('doi')
            component.doi_resource = doi_resource
        
        # Append it to our list of components
        component_list.append(component)

    return component_list


def remove_tag(tag_name, string):

    """
    Remove unwanted tags from the string, keeping the contents it surrounds,
    parsing it as HTML, then only keep the body paragraph contents
    """
    if string is None:
        return None
    
    soup = BeautifulSoup(string)

    tags = soup.find_all(tag_name)
    for tag in tags:
        tag.unwrap()
    
    # If the abstract starts with a tag, then it will not be enclosed in a p tag
    if hasattr(soup.body.p, "children"):
        return "".join(map(unicode, soup.body.p.children)) or None
    elif hasattr(soup.body, "children"):
        # No p tag, use all the children
        return "".join(map(unicode, soup.body.children)) or None
    else:
        return None

def clean_abstract(abstract):
    """
    Remove unwanted tags from abstract string,
    parsing it as HTML, then only keep the body paragraph contents
    """

    remove_tags = ['xref', 'ext-link']
    for tag_name in remove_tags:
        abstract = remove_tag(tag_name, abstract)
    
    return abstract


def build_article_from_xml(article_xml_filename):
    """
    Parse JATS XML with elifetools parser, and populate an
    eLifePOA article object
    Basic data crossref needs: article_id, doi, title, contributors with names set
    """
    
    error_count = 0
    
    soup = parser.parse_document(article_xml_filename)
    
    # Get DOI
    doi = parser.doi(soup)
    
    # Create the article object
    article = eLifePOA(doi, title=None)
    
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
    
    # contributors
    contrib_type = "author"
    authors = parser.authors(soup, contrib_type)
    contributors = build_contributors(authors, contrib_type)
    article.contributors = contributors
    
    contrib_type = "author non-byline"
    authors = parser.authors(soup, contrib_type)
    contributors_non_byline = build_contributors(authors, contrib_type)
    article.contributors = article.contributors + contributors_non_byline
    
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
    award_groups = parser.full_award_groups(soup)
    article.funding_awards = build_funding(award_groups)
    
    # references or citations 
    refs = parser.refs(soup)
    article.ref_list = build_ref_list(refs)
    
    # components with component DOI 
    components = parser.components(soup)
    article.component_list = build_components(components)
        
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

    return article,error_count


def build_articles_from_article_xmls(article_xmls):
    """
    Given a list of article XML filenames, convert to article objects
    """

    poa_articles = []
    
    for article_xml in article_xmls:
        print "working on ", article_xml
        article,error_count = build_article_from_xml(article_xml)
        if error_count == 0:
            poa_articles.append(article)
            
    return poa_articles

if __name__ == '__main__':
    
    article_xlms = [#"elife_poa_e02935.xml"
                    #,"Feature.xml"
                    "elife_poa_e02923.xml"
                    ,"elife00003.xml"
                    ,"elife02676.xml"
                    ]
    poa_articles = []
    
    for article_xml in article_xlms:
        print "working on ", article_xml
        article,error_count = build_article_from_xml("generated_xml_output" + os.sep + article_xml)
        
        if error_count == 0:
            poa_articles.append(article)
        print article.doi




