import xml
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
import time
import datetime
import calendar
import re
import os
from generatePoaXml import *
import settings

"""
Parse PoA XML file and can instantiate a eLifePOA object from the data
"""

def convert_element_to_string(parent, xml_string, recursive = False):
    """
    Recursively,
    Given an ElementTree.Element as parent,
    append the tags and content from xml to the string
    Used primarily for parsing XML with <italic> tags
    Does not include tag attributes
    """

    tag_count = 0
    sub_xml_string = ''
    
    # Iterate over child tags, if present, and call recursively
    for child in parent:
        sub_xml_string += convert_element_to_string(child, xml_string, True)
        tag_count = tag_count + 1
    
    # Add the recursive xml to the main xml_string
    xml_string += sub_xml_string

    if tag_count > 0:
        # Add text to start of the string and tail to the end
        if parent.text:
            xml_string = parent.text + xml_string

        if parent.tail:
            xml_string = xml_string + parent.tail 

    elif tag_count == 0:
        # No nested tags, add the tag to the string
        if recursive is True:
            # Only add nested tags, not the parent tag
            xml_string += '<' + parent.tag + '>'

        if parent.text:
            xml_string += parent.text
        
        if recursive is True:
            xml_string += '</' + parent.tag + '>'
     
        if parent.tail:
            xml_string += parent.tail
            
    return xml_string

def strip_tags_from_string(str):
    """
    Given a string of XML, remove all the tags and return
    the content between the tags
    """
    
    str_stripped = ''
    # Remove all tags to leave the content behind
    aff_chunks = re.split('(<.*?>)', str)
    for chunk in aff_chunks:
        if chunk.count('<') <= 0 and chunk.count('>') <= 0:
            str_stripped += chunk
    return str_stripped

def get_article_id_from_xml(root, pub_id_type = "publisher-id"):
    """
    Given an xml.etree.ElementTree.Element, get the
    article_id
    of a pub_id_type
    """
    article_id = None
    for tag in root.findall('./front/article-meta/article-id'):
        if tag.get("pub-id-type") == "publisher-id":
            #print "article_id: " + tag.text
            article_id = int(tag.text)
        elif tag.get("pub-id-type") == "doi":
            #print "doi: " + tag.text
            article_id = tag.text
    return article_id

def get_title_from_xml(root):
    """
    Given an xml.etree.ElementTree.Element, get the
    title
    """
    title = None
    for tag in root.findall('./front/article-meta/title-group/article-title'):
        # Recursively flatten child elements into a string
        title = convert_element_to_string(tag, '').encode('utf-8')
        
    return title
    
def get_abstract_from_xml(root):
    """
    Given an xml.etree.ElementTree.Element, get the
    abstract
    """
    abstract = None
    for tag in root.findall('./front/article-meta/abstract'):
        # Recursively flatten child elements into a string
        if not tag.get("abstract-type"):
            abstract = convert_element_to_string(tag, u'').encode('utf-8')

    return abstract

def get_affs_from_xml(root):
    """
    Given an xml.etree.ElementTree.Element, get the
    aff
    tag content 
    """

    affs = {}
    for tag in root.findall('./front/article-meta/contrib-group/aff'):
        id = tag.get("id")
        #print id
        aff_with_tags = convert_element_to_string(tag, '').encode('utf-8')
        
        # Remove the <label> tag and contents
        # TODO!!!!!!
        
        # Remove all tags to leave the content behind
        aff = strip_tags_from_string(aff_with_tags)
        
        affs[id] = aff

    return affs


def get_contributor_from_contrib_group(root, affs):
    """
    Given an xml.etree.ElementTree.Element, get the
    contributor object details and instantiate and object
    """
    contributor = None
    
    contrib_type = root.get("contrib-type")
    affiliations = []
    
    for tag in root.findall('./name/surname'):
        surname = tag.text
        
    for tag in root.findall('./name/given-names'):
        given_name = tag.text
    
    # PoA may have aff tags
    for tag in root.findall('./aff'):
        aff = ''
        # 1. Convert all content and tags to a string
        aff_with_tags = convert_element_to_string(tag, '').encode('utf-8')
        # 2. Remove all tags to leave the content behind
        aff = strip_tags_from_string(aff_with_tags)
        
        affiliations.append(aff)

    # VoR may have xref to aff tags
    if len(affs) > 0:
        
        for tag in root.findall('./xref'):
            if tag.get("ref-type") == "aff":
                
                rid = tag.get("rid")
                #print rid
                try:
                    affiliations.append(affs[rid])
                except:
                    # key error
                   continue

    # Instantiate
    contributor = eLifePOSContributor(contrib_type, surname, given_name)
    
    for aff in affiliations:
        contributor.set_affiliation(aff)
    
    if root.get("corresp") == "yes":
        contributor.corresp = True

    return contributor

def get_contributors_from_xml(root, contrib_type = None):
    """
    Given an xml.etree.ElementTree.Element, get the
    contributors
    contrib_type can be author, editor, etc.
    """
    contributors = []

    # VoR may have xref to aff tags
    affs = get_affs_from_xml(root)

    for tag in root.findall('./front/article-meta/contrib-group/contrib'):
        contributor = None
        if not contrib_type:
            contributor = get_contributor_from_contrib_group(tag, affs)
        elif tag.get("contrib-type") == contrib_type:
            contributor = get_contributor_from_contrib_group(tag, affs)
        
        if contributor:
            contributors.append(contributor)  

    return contributors

def get_history_from_xml(root, contrib_type = None):
    """
    Given an xml.etree.ElementTree.Element, get the
    history
    and return types of dates and their time.struct_time representation
    """
    history = {}
    for tag in root.findall('./front/article-meta/history/date'):
        date_type = tag.get("date-type")
        for child in tag:
            if child.tag == 'day':
                day = child.text
            elif child.tag == 'month':
                month = child.text
            elif child.tag == 'year':   
                year = child.text

        # Create the time object
        try:
            date = datetime.datetime(int(year), int(month), int(day))
        except:
            date = None
            
        if date:
            history[date_type] = date.timetuple()

    return history

def get_pub_dates_from_xml(root, contrib_type = None):
    """
    Given an xml.etree.ElementTree.Element, get all the
    pub-date
    elements and return types of dates and their time.struct_time representation
    """
    pub_dates = {}
    for tag in root.findall('./front/article-meta/pub-date'):
        pub_type = tag.get("pub-type")
        for child in tag:
            if child.tag == 'day':
                day = child.text
            elif child.tag == 'month':
                month = child.text
            elif child.tag == 'year':   
                year = child.text

        # Create the time object
        try:
            date = datetime.datetime(int(year), int(month), int(day))
        except:
            date = None
            
        if date:
            pub_dates[pub_type] = date.timetuple()

    return pub_dates

def get_license_from_xml(root, contrib_type = None):
    """
    Given an xml.etree.ElementTree.Element, get the
    license
    and return the license details
    """
    license = {}
    license['href'] = None
    
    # Get the license href
    for tag in root.findall('./front/article-meta/permissions/license'):
        license['href'] = tag.get("{http://www.w3.org/1999/xlink}href")
            
    return license

def build_article_from_xml(article_xml_filename):
    """
    Parse NLM XML with ElementTree, and populate an
    eLifePOA article object
    Basic data crossref needs: article_id, doi, title, contributors with names set
    """
    
    error_count = 0
    
    tree = ElementTree.parse(article_xml_filename)
    root = tree.getroot()

    # Get DOI and article_id
    article_id = get_article_id_from_xml(root, "publisher-id")
    doi = get_article_id_from_xml(root, "doi")
    
    # Create the article object
    article = eLifePOA(doi, title=None)
    
    # title
    article.title = get_title_from_xml(root)
    #print article.title
        
    # abstract
    article.abstract = get_abstract_from_xml(root)
    
    # contributors
    contributors = get_contributors_from_xml(root, contrib_type = "author")
    article.contributors = contributors
    
    # license href
    license_data = get_license_from_xml(root)
    license = eLifeLicense()
    license.href = license_data['href']
    article.license = license
    
    history_dates = get_history_from_xml(root)
    
    date_types = ["received", "accepted"]
    for date_type in date_types:
        try:
            if history_dates[date_type]:
                date_instance = eLifeDate(date_type, history_dates[date_type])
                article.add_date(date_instance)
        except KeyError:
            # date did not exist
            error_count = error_count + 1
            
    # Parse the pub-date for VoR articles
    pub_dates = get_pub_dates_from_xml(root)
    pub_date_types = ["epub"]
    for pub_type in pub_date_types:
        try:
            if pub_dates[pub_type]:
                date_instance = eLifeDate(pub_type, pub_dates[pub_type])
                article.add_date(date_instance)
        
        except:
            # PoA will not have pub-date, quietly continue
            pass

    return article,error_count

if __name__ == '__main__':
    
    article_xlms = ["elife_poa_e03011.xml"
                    ,"elife_poa_e03198.xml"
                    ,"elife_poa_e03191.xml"
                    ,"elife_poa_e03300.xml"
                    ,"elife_poa_e02676.xml"
                    ]
    poa_articles = []
    
    for article_xml in article_xlms:
        print "working on ", article_xml
        article,error_count = build_article_from_xml("generated_xml_output" + os.sep + article_xml)
        
        if error_count == 0:
            poa_articles.append(article)
        print article.doi




