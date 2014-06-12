from lettuce import *
from generatePoaXml import *
import parseCSVFiles
import json
from xml.etree import ElementTree

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

@step(u'I have settings')
def i_have_settings(step):
    world.settings = settings
    assert world.settings is not None, \
        "Got settings %s" % world.settings

@step(u'I read settings (\S+)')
def i_read_settings_property(step, property):
    world.value = getattr(world.settings, property)
    assert world.value is not None, \
        "Got value %s" % world.value

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
    attr = None
    setattr(world.settings, property, value)
    attr = getattr(world.settings, property)
    assert attr is not None, \
        "Got attr %s" % str(attr)
    
@step(u'I set json settings (\S+) to (.*)')
def i_set_json_settings_property_to_value(step, property, value):
    attr = None
    setattr(world.settings, property, json.loads(str(value)))
    attr = getattr(world.settings, property)
    assert attr is not None, \
        "Got attr %s" % str(attr)
    
@step(u'I reload settings')
def i_reload_settings(step):
    reload(world.settings)
    assert world.settings is not None, \
        "Got settings %s" % world.settings
    
@step(u'I reload XML generation libraries')
def i_reload_xml_generation_libraries(step):
    reload(parseCSVFiles)
    assert world.settings is not None, \
        "Got settings %s" % world.settings
    
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
        attribute = str(attribute)
    elif type(world.attribute) == int:
        attribute = int(attribute)
    elif type(world.attribute) == list:
        attribute = attribute.split(",")
    # Compare value
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

    
    