# -*- coding: utf-8 -*-
from lettuce import *
from parsePoaXml import *
import os

test_xml_path = world.basedir + os.sep + 'tests' + os.sep +  "test_data" + os.sep

@step('I have the document (\S+)')
def have_the_document(step, document):
    world.document = document
    world.file_location = set_file_location(document)

@step(u'I build article from xml')
def i_build_article_from_xml(step):
    (world.article, world.error_count) = build_article_from_xml(world.file_location)
    assert world.article is not None, \
        "Got article %s" % world.article

@step(u'I have errors (\S+)')
def i_have_errors(step, errors):
    if errors == "True":
        world.errors = True
    elif errors == "False":
        world.errors = False
    
    has_errors = None
    if world.error_count > 0:
        has_errors = True
    elif world.error_count <= 0:
        has_errors = False
    
    assert world.errors == has_errors, \
        "Got has_errors %s" % has_errors

@step(u'I have the attribute (.*)')
def i_have_the_attribute(step, attribute):
    world.attribute = attribute
    assert world.attribute is not None, \
        "Got attribute %s" % world.attribute

@step(u'I set the object to article$')
def i_set_the_object_to_the_article(step):
    world.object = world.article
    assert world.object is not None, \
        "Got contributor %s" % world.object

@step(u'I set the object to article contributor index (.*)')
def i_set_the_object_to_article_contributor_index(step, index):
    world.object = world.article.contributors[int(index)]
    assert world.object is not None, \
        "Got contributor %s" % world.object

@step(u'I set the object to article license index (.*)')
def i_set_the_object_to_article_license_index(step, index):
    # Index is ignored
    world.object = world.article.license
    assert world.object is not None, \
        "Got contributor %s" % world.object
    
@step(u'I set the object to article article_categories index (.*)')
def i_set_the_object_to_article_article_categories_index(step, index):
    world.object = world.article.article_categories[int(index)]
    assert world.object is not None, \
        "Got contributor %s" % world.object
    
@step(u'I set the object to article author_keywords index (.*)')
def i_set_the_object_to_article_author_keywords_index(step, index):
    world.object = world.article.author_keywords[int(index)]
    assert world.object is not None, \
        "Got contributor %s" % world.object 
    
@step(u'I set the object to article research_organisms index (.*)')
def i_set_the_object_to_article_research_organisms_index(step, index):
    world.object = world.article.research_organisms[int(index)]
    assert world.object is not None, \
        "Got contributor %s" % world.object
    


@step(u'I have object attribute value (.*)')
def i_have_object_attribute_value(step, value):
    if value == "None":
        value = None
    if value == "False":
        value = False
    if value == "True":
        value = True
    
    if world.attribute:
        object_value = getattr(world.object, world.attribute, None)
    else:
        object_value = world.object
        
    assert value == object_value, \
        "Got object value %s" % object_value


def set_file_location(doc):
    document = doc.lstrip('"').rstrip('"')
    file_location = test_xml_path + document
    return file_location
