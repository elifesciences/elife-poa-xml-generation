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
from elifetools import parseJATS as parser

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

def get_article_type_from_xml(root):
    """
    Given an xml.etree.ElementTree.Element, get the
    article-type
    of a article, the root element
    """
    article_type = None
    try:
        article_type = root.get("article-type")
    except:
        pass

    return article_type

def get_article_id_from_xml(root, pub_id_type = "publisher-id"):
    """
    Given an xml.etree.ElementTree.Element, get the
    article_id
    of a pub_id_type
    """
    article_id = None
    for tag in root.findall('./front/article-meta/article-id'):
        if tag.get("pub-id-type") == pub_id_type:
            #print "article_id: " + tag.text
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
        title = convert_element_to_string(tag, '')
        
    return title
    
def get_abstract_from_xml(root, raw = False):
    """
    Given an xml.etree.ElementTree.Element, get the
    abstract
    """
    abstract = None
    for tag in root.findall('./front/article-meta/abstract'):
        
        if not raw:
            # Remove unallowed tags and their contents
            for remove_tag in tag.findall('./object-id'):
                tag.remove(remove_tag)
            # Some tags are nested inside p tag
            for p_tag in tag.findall('./p'):
                for remove_tag in p_tag.findall('./bold'):
                    p_tag.remove(remove_tag)
                for remove_tag in p_tag.findall('./ext-link'):
                    p_tag.remove(remove_tag)
            # Now remove any empty p tags with no child tags
            for p_tag in tag.findall('./p'):
                if p_tag.text is None and len(p_tag) <= 0:
                    tag.remove(p_tag)
                # Remove nested xref tags but leave the text inside
                for xref_tag in p_tag.findall('./xref'):
                    # Two step process
                    # One, remove all attributes of the xref tag
                    # Two (later) remove empty xref tags from the converted string
                    for attr in xref_tag.keys():
                        xref_tag.set(attr, None)
        
        # Recursively flatten child elements into a string
        if not tag.get("abstract-type"):
            abstract = convert_element_to_string(tag, '')
            
        if not raw:
            # Finally, remove excess <p> and </p> tags because they are bad
            abstract = abstract.replace('<p>', '')
            abstract = abstract.replace('</p>', '')
            abstract = abstract.replace('<xref>', '')
            abstract = abstract.replace('</xref>', '')

    return abstract

def get_affs_from_xml(root, raw = False):
    """
    Given an xml.etree.ElementTree.Element, get the
    aff
    tag content
    Pass raw = true to not remove certain tags
    """

    affs = {}
    for tag in root.findall('./front/article-meta/contrib-group/aff'):
        id = tag.get("id")
        
        if not raw:
            # Remove the <label> tag and contents
            for remove_tag in tag.findall('./label'):
                tag.remove(remove_tag)
        
        #print id
        aff_with_tags = convert_element_to_string(tag, '')

        # Remove all tags to leave the content behind
        aff = {}
        aff["text"] = strip_tags_from_string(aff_with_tags)
        
        affs[id] = aff

    return affs


def get_contributor_from_contrib_group(root, affs, raw = False):
    """
    Given an xml.etree.ElementTree.Element, get the
    contributor object details and instantiate and object
    """
    contributor = None
    
    contrib_type = root.get("contrib-type")
    affiliations = []
    orcid = None
    surname = None
    given_name = None
    collab = None
    group_author_key = None
    
    for tag in root.findall('./name/surname'):
        surname = tag.text
        
    for tag in root.findall('./name/given-names'):
        given_name = tag.text
    
    for tag in root.findall('./collab'):
        collab = tag.text
    
    for tag in root.findall('./contrib-id'):
        if tag.get("contrib-id-type") == "orcid":
            orcid = tag.text
    
    for tag in root.findall('./contrib-id'):
        if tag.get("contrib-id-type") == "group-author-key":
            group_author_key = tag.text
    
    # PoA may have aff tags
    for tag in root.findall('./aff'):
        aff = ''
        
        if not raw:
            # Do not need email
            for remove_tag in tag.findall('./email'):
                tag.remove(remove_tag)
        
        # 1. Convert all content and tags to a string
        aff_with_tags = convert_element_to_string(tag, '')
        # 2. Remove all tags to leave the content behind
        aff = {}
        aff["text"] = strip_tags_from_string(aff_with_tags)
        
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
    contributor = eLifePOSContributor(contrib_type, surname, given_name, collab)
    
    for aff in affiliations:
        affiliation = ContributorAffiliation()
        affiliation.text = aff["text"]
        contributor.set_affiliation(affiliation)
    
    if root.get("corresp") == "yes":
        contributor.corresp = True
    contributor.orcid = orcid
    contributor.group_author_key = group_author_key
    
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
        pub_type = tag.get("date-type")
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

def get_subject_groups_from_xml(root, subj_group_type = None):
    """
    Given an xml.etree.ElementTree.Element, get the
    subj-group
    values, optionally filtered by subj-group-type
    """
    subject_groups = []
    
    for tag in root.findall('./front/article-meta/article-categories/subj-group'):
        add_tag = None
        
        if subj_group_type:
            if tag.get("subj-group-type") == subj_group_type:
                add_tag = True
        else:
            add_tag = True
            
        if add_tag:
            for s_tag in tag.findall('./subject'):
                subject_groups.append(s_tag.text)

    return subject_groups

def get_keyword_groups_from_xml(root, kwd_group_type = None):
    """
    Given an xml.etree.ElementTree.Element, get the
    kwd-group
    values, optionally filtered by kwd-group-type
    """
    keyword_groups = []
    
    for tag in root.findall('./front/article-meta/kwd-group'):
        add_tag = None
        
        if kwd_group_type:
            if tag.get("kwd-group-type") == kwd_group_type:
                add_tag = True
        else:
            add_tag = True
            
        if add_tag:
            for k_tag in tag.findall('./kwd'):
                # Check for nested italic tag
                child_count = 0
                for child in k_tag:
                    keyword_groups.append(child.text)
                    child_count = child_count + 1
                # If there are no nested tags use the base text
                if child_count == 0:
                    keyword_groups.append(k_tag.text)

    return keyword_groups

def get_volume_from_xml(root, contrib_type = None):
    """
    Given an xml.etree.ElementTree.Element, get the
    volume
    if present and return it
    """
    volume = None
    
    for tag in root.findall('./front/article-meta/volume'):
        volume = tag.text

    return volume

def get_is_poa_from_xml(root, contrib_type = None):
    """
    Given an xml.etree.ElementTree.Element, get the
    pub-date pub-type="collection"
    if present then is_poa is false, if not present then is_poa is True
    """
    # Default value
    is_poa = True
    
    # When parsing the file, use the presence of a
    #   pub-date pub-type="collection"   as is_poa is False, other wise is_poa is True

    for tag in root.findall('./front/article-meta/pub-date'):
        pub_type = tag.get("pub-type")
        if pub_type == "collection":
            is_poa = False
    
    return is_poa

def build_article_from_xml(article_xml_filename):
    """
    Parse NLM XML with ElementTree, and populate an
    eLifePOA article object
    Basic data crossref needs: article_id, doi, title, contributors with names set
    """
    
    error_count = 0
    
    tree = ElementTree.parse(article_xml_filename)
    root = tree.getroot()

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
    article.abstract = parser.full_abstract(soup)
    
    # contributors
    contributors = get_contributors_from_xml(root, contrib_type = "author")
    article.contributors = contributors
    contributors_non_byline = get_contributors_from_xml(root, contrib_type = "author non-byline")
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
                    ]
    poa_articles = []
    
    for article_xml in article_xlms:
        print "working on ", article_xml
        article,error_count = build_article_from_xml("generated_xml_output" + os.sep + article_xml)
        
        if error_count == 0:
            poa_articles.append(article)
        print article.doi




