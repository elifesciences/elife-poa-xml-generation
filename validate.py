from StringIO import StringIO
from lxml import etree
import requests 

#NLM DTD is at http://dtd.nlm.nih.gov/archiving/3.0/archivearticle3.dtd 
r = requests.get('http://dtd.nlm.nih.gov/archiving/3.0/archivearticle3.dtd')
NLM_DTD = r.text 

dtd = etree.DTD(StringIO(NLM_DTD))
root = etree.XML("<foo/>")
print(dtd.validate(root))
# True

root = etree.XML("<foo>bar</foo>")
print(dtd.validate(root))
# False
print(dtd.error_log.filter_from_errors())
# <string>:1:0:ERROR:VALID:DTD_NOT_EMPTY: Element foo was declared EMPTY this one has content


# #!/usr/bin/python -u
# import libxml2
# import sys

# # Memory debug specific
# libxml2.debugMemory(1)

# dtd="""<!ELEMENT foo EMPTY>"""
# instance="""<?xml version="1.0"?>
# <foo></foo>"""

# dtd = libxml2.parseDTD(None, 'test.dtd')
# ctxt = libxml2.newValidCtxt()
# doc = libxml2.parseDoc(instance)
# ret = doc.validateDtd(ctxt, dtd)
# if ret != 1:
#     print "error doing DTD validation"
#     sys.exit(1)

# doc.freeDoc()
# dtd.freeDtd()
# del dtd
# del ctxt 