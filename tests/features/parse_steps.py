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

@step(u'I have the attribute (\S+)')
def i_have_the_attribute(step, attribute):
    world.attribute = attribute
    assert world.attribute is not None, \
        "Got attribute %s" % world.attribute
    
@step(u'I have article attribute value (.*)')
def i_have_article_attribute_value(step, value):
    val = getattr(world.article, world.attribute, None)
    assert value == val, \
        "Got val %s" % val






def set_file_location(doc):
    document = doc.lstrip('"').rstrip('"')
    file_location = test_xml_path + document
    return file_location
