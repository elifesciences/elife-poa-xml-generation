from lettuce import *
from generatePoaXml import *

@step(u'I have the string (.*)')
def i_have_the_string_string(step, string):
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
    
@step(u'I set settings (\S+) to (.*)')
def i_set_settings_property_to_value(step, property, value):
    attr = None
    setattr(world.settings, property, value)
    attr = getattr(world.settings, property)
    assert attr is not None, \
        "Got attr %s" % str(attr)
    
@step(u'I reload settings')
def i_reload_settings(step):
    reload(world.settings)
    assert world.settings is not None, \
        "Got settings %s" % world.settings