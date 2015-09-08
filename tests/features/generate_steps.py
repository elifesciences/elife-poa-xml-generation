from lettuce import *
from generatePoaXml import *
import parseCSVFiles
from xml_generation import *
import json
from xml.etree import ElementTree

# Default XLS_FILES for using in tests when required
XLS_FILES = {"authors" : "poa_author.csv", "license" : "poa_license.csv", "manuscript" : "poa_manuscript.csv", "received" : "poa_received.csv", "subjects" : "poa_subject_area.csv", "organisms": "poa_research_organism.csv", "abstract": "poa_abstract.csv", "title": "poa_title.csv", "keywords": "poa_keywords.csv", "group_authors": "poa_group_authors.csv"}

@step(u'I have the string (\S+)')
def i_have_the_string_string(step, string):
    world.string = string
    assert world.string is not None, \
        "Got string %s" % world.string
    
@step(u'I have the raw string (.*)')
def i_have_the_raw_string(step, string):
    world.string = string
    assert world.string is not None, \
        "Got string %s" % world.string
    
@step(u'I convert the string with entities to unicode')
def i_convert_the_string_with_entities_to_unicode(step):
    world.unicode_string = entity_to_unicode(world.string)
    assert world.unicode_string is not None, \
        "Got unicode_string %s" % world.unicode_string
    
@step(u'I have the unicode (.*)')
def i_have_the_unicode(step, unicode_string):
    assert world.unicode_string == unicode_string, \
        "Got unicode_string %s" % world.unicode_string

@step(u'I decode the string with decode brackets')
def i_decode_the_string_with_decode_brackets(step):
    world.decoded_string = decode_brackets(world.string)
    assert world.decoded_string is not None, \
        "Got decoded_string %s" % world.decoded_string
    
@step(u'I have the decoded string (.*)')
def i_have_the_decoded_string_decoded_string(step, decoded_string):
    assert world.decoded_string == decoded_string, \
        "Got decoded_string %s" % world.decoded_string

@step(u'I read settings (\S+)')
def i_read_settings_property(step, property):
    world.value = getattr(settings, property)
    assert world.value is not None, \
        "Got value %s" % world.value

@step(u'I import (\S+)')
def i_import(step, library):
    import importlib
    mod = importlib.import_module(library)
    setattr(world, library, mod)
    assert getattr(world, library) is not None, \
        "Got value %s" % getattr(world, library)

@step(u'I have the value (.*)')
def i_have_the_value(step, value):
    # Type convert the value as required
    if type(world.value) == str:
        value = str(value)
    elif type(world.value) == int:
        value = int(value)
    # Compare value
    assert world.value == value, \
        "Got value %s" % world.value
    
@step(u'I have the json value (.*)')
def i_have_the_json_value(step, value):
    assert json.loads(value) == world.value, \
        "Got value %s" % world.value
    
@step(u'I set settings (\S+) to (.*)')
def i_set_settings_property_to_value(step, property, value):
    setattr(settings, property, value)
    attr = getattr(settings, property)
    assert attr is not None, \
        "Got attr %s" % str(attr)
    
@step(u'I set json settings (\S+) to (.*)')
def i_set_json_settings_property_to_value(step, property, value):
    setattr(settings, property, json.loads(str(value)))
    attr = getattr(settings, property)
    assert attr is not None, \
        "Got attr %s" % str(attr)
    
@step(u'I set XLS_FILES to the default')
def i_set_xls_files_to_the_default(step):
    # Set to the default so it does not need to be repeated
    property = "XLS_FILES"
    setattr(settings, property, XLS_FILES)
    attr = getattr(settings, property)
    assert attr is not None, \
        "Got attr %s" % str(attr)
    
@step(u'I reload settings')
def i_reload_settings(step):
    reload(settings)
    assert settings is not None, \
        "Got settings %s" % settings
    
@step(u'I reload XML generation libraries')
def i_reload_xml_generation_libraries(step):
    reload(parseCSVFiles)
    assert parseCSVFiles is not None, \
        "Got parseCSVFiles %s" % parseCSVFiles
    
@step(u'I have article_id (\S+)')
def i_have_article_id(step, article_id):
    world.article_id = article_id
    assert world.article_id is not None, \
        "Got article_id %s" % world.article_id
    
@step('I have author_id (.*)')
def i_have_author_id(step, author_id):
    world.author_id = author_id
    assert world.author_id is not None, \
        "Got author_id %s" % world.author_id
    
@step(u'I set attribute to parseCSVFiles method (\S+)')
def i_set_attribute_to_parsecsvfiles_method(step, method_name):
    method = getattr(parseCSVFiles, method_name)
    if world.author_id != "":
        world.attribute = method(str(int(world.article_id)), str(int(world.author_id)))
    else:
        world.attribute = method(str(int(world.article_id)))
        
    assert world.attribute is not None, \
        "Got attribute %s" % method_name + world.article_id
   
@step(u'I have attribute (.*)')
def i_have_attribute_attribute(step, attribute):
    # Type convert the value as required
    if type(world.attribute) == str:
        # Test for explicit empty string
        if attribute == '" "':
            attribute = " "
        try:
            attribute = str(attribute)
        except UnicodeEncodeError:
            attribute = attribute.encode('utf-8')
        
    elif type(world.attribute) == int:
        attribute = int(attribute)
    elif type(world.attribute) == list:
        attribute = attribute.split(",")
    # Compare value
    if world.attribute is True or world.attribute is False:
        # Compare strings when it is boolean, seems to be the best working option
        assert str(world.attribute) == str(attribute), \
            "Got attribute %s" % world.attribute
    else:
        assert world.attribute == attribute, \
            "Got attribute %s" % world.attribute
    
@step(u'I tag replace the decoded string')
def i_tag_replace_the_decoded_string(step):
    string = replace_tags(world.decoded_string)
    world.decoded_string = string
    assert string is not None, \
        "Got string %s" % string
    
@step(u'I surround the decoded string with tag_name (.*)')
def i_surround_the_decoded_string_with_tag_name(step, tag_name):
    world.tag_name = tag_name
    tagged_string = '<' + tag_name + '>' + world.decoded_string + '</' + tag_name + '>'
    world.decoded_string = tagged_string
    assert tagged_string is not None, \
        "Got tagged_string %s" % tagged_string
    
@step(u'I have the root xml element')
def i_have_the_root_xml_element(step):
    world.root_xml_element = Element('root')
    assert world.root_xml_element is not None, \
        "Got root_xml_element %s" % world.root_xml_element
  
@step(u'I convert the decoded string to an xml element')
def i_convert_the_decoded_string_to_an_xml_element(step):
    reparsed = minidom.parseString(world.decoded_string)
    world.xml_element = reparsed
    assert world.xml_element is not None, \
        "Got xml_element %s" % p_node.childNodes[0] + p_node.childNodes[1]
    
@step('I have xml element string (.*)')
def i_have_xml_element_string(step, xml_elem_string):
    encoding = 'utf-8'
    xml_str = world.xml_element.toprettyxml(indent="", newl="")

    assert unicode(xml_str) == xml_elem_string, \
        "Got xml_elem_string %s" % xml_str
    
@step(u'I append the xml element to the root xml element')
def i_append_the_xml_element_to_the_root_xml_element(step):
    
    world.root_xml_element = append_minidom_xml_to_elementtree_xml(
        world.root_xml_element, world.xml_element
        )
    
    #encoding = 'utf-8'
    #print ElementTree.tostring(world.root_xml_element, encoding)
    assert world.root_xml_element is not None, \
        "Got root_xml_element %s" % world.root_xml_element
   
@step(u'I copy string to world decoded string')
def i_copy_string_to_world_decoded_string(step):
    world.decoded_string = world.string
    assert world.decoded_string is not None, \
        "Got decoded_string %s" % world.decoded_string
    
@step(u'I escape unmatched angle brackets')
def i_escape_unmatched_angle_brackets(step):
    world.decoded_string = escape_unmatched_angle_brackets(world.decoded_string)
    assert world.decoded_string is not None, \
        "Got decoded_string %s" % world.decoded_string

@step(u'I convert the root xml element to string')
def i_convert_the_root_xml_element_to_string(step):
    encoding = 'utf-8'
    rough_string = ElementTree.tostring(world.root_xml_element, encoding)
    reparsed = minidom.parseString(rough_string)
    world.xml_string = reparsed.toxml()
    assert world.xml_string is not None, \
        "Got xml_string %s" % world.xml_string
    
@step(u'I have the xml string (.*)')
def i_have_the_xml_string_xml_string(step, xml_string):
    assert world.xml_string == xml_string, \
        "Got xml_string %s" % world.xml_string

@step(u'I build POA XML for article')
def i_build_poa_xml_for_article(step):
    world.attribute = build_xml_for_article(int(world.article_id))
    assert world.attribute is True, \
        "Got attribute %s" % world.attribute
    
@step(u'I build POA article for article')
def i_build_poa_article_for_article(step):
    world.article, error_count = build_article_for_article(int(world.article_id))
    assert world.article is not None, \
        "Got article %s" % world.article

@step(u'I have as list index')
def i_have_as_list_index_none(step):
    # When no index is supplied set it to None
    world.index = None
    assert world.index is None, \
        "Got index %s" % world.index

@step(u'I have as list index (\d+)')
def i_have_as_list_index(step, index):
    world.index = int(index)
    assert world.index is not None, \
        "Got index %s" % world.index

@step(u'I have sub property')
def i_have_sub_property_none(step):
    # When no subproperty is supplied set it to None
    world.subproperty = None
    assert world.subproperty is None, \
        "Got subproperty %s" % world.subproperty

@step(u'I have sub property (\S+)')
def i_have_sub_property_subproperty(step, subproperty):
    if subproperty == "":
        # When no sub_property is supplied set it to None
        world.subproperty = None
        assert world.subproperty is None, \
            "Got subproperty %s" % world.subproperty
    else:
        world.subproperty = subproperty
        assert world.subproperty is not None, \
            "Got subproperty %s" % world.subproperty

@step(u'I set attribute to article object property (\S+)')
def i_set_attribute_to_article_object_property(step, property):
    # Set the attribute to article object property with optional list index
    if world.index is not None:
        list_property = getattr(world.article, property)
        attribute = list_property[world.index]
    else:
        attribute = getattr(world.article, property)

    # Get the property of the attribute if we want a sub_property
    if world.subproperty is not None:
        world.attribute = getattr(attribute, world.subproperty)
    else:
        world.attribute = attribute
        
    assert world.attribute is not None, \
        "Got attribute %s" % world.attribute
    
@step(u'I parse group authors')
def i_parse_group_authors(step):
    world.attribute = parse_group_authors(world.string)
    assert world.attribute is not None, \
        "Got attribute %s" % world.attribute
    
@step(u'I set attribute to attribute index (\d+)')
def i_set_attribute_to_attribute_index(step, index):
    world.attribute = world.attribute[index]
    assert world.attribute is not None, \
        "Got attribute %s" % world.attribute
    
    