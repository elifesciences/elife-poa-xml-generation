# Background

This is a project to create XML files that conform to the output we expect for delivery to HighWire for the publish on accept project. 


## Goal

The goal is to have a functioning pipeline in place to delivery XML to HW before the end of December 2013. 

## Resources and project planning. 

- [Overview of project resources](https://github.com/elifesciences/elifesciences-wiki/wiki/Elife-POA-XML-Project).
- [Links to useful documentation on XML generation in Python](./RESOURCES.md)

## Project dependencies

	$ pip install elementtree  
	$ pip install http://svn.effbot.org/public/elementtree-1.3/  

## Project outline 

#### Data directories

- `sample-xls-input` - contains example output from EJP SQL query  
- `sample-xml-generated-output` - place xml that our script generates into this directory
- `sample-xml-required-output` - contains the XML specification from production, our generated XML should match the format of the XML in this directory  

#### Python scripts

- `elife_poa_xls2xml.py` hard codes reading `sample-xls-input/eLife_query_tool_508.xls` and generates output XML. Includes helper functions for reading from an XLS file, imports classes for XML modelling from `generatePoaXml.py`     
- `generatePoaXml.py` set of classes for modelling the output XML  
- `parseXls.py` toy example for reading from and XLS file, not used  
- `validate.py` toy example of generating a validation script, not used  

#### Generating XML from and XLS file

	$ python elife_poa_xls2xml.py > sample-xml-generated-output/outputName.xml 


#### Verifying XML file

	$ xmllint --noout --loaddtd --valid sample-xml-generated-output/outputName.xml




## Project issues

Live code issues are listed as issues in the [git repo for this project](https://github.com/elifesciences/elife-poa-xml-generation/issues).



# Version history 

2013-12-09 inital batch of code ready to review.   
2013-11-26 first proof of concept.   
