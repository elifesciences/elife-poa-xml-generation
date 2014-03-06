# Background

This is a project to create XML files that conform to the output we expect for delivery to HighWire for the publish on accept project.


## Goal

The goal is to have a functioning pipeline in place to delivery XML to HW before the end of December 2013.

## Quickstart

- set paths in settings.py
- run `$ python xml_generation.py`

## Resources and project planning.

- [Overview of project resources](https://github.com/elifesciences/elifesciences-wiki/wiki/Elife-POA-XML-Project).
- [Links to useful documentation on XML generation in Python](./RESOURCES.md)

## Project dependencies

	$ pip install elementtree  
	$ pip install xlrd
	$ pip install gitpython
	$ pip install PIL==1.1.7
	$ pip install PyPDF2==1.20
	$ pip install reportlab==3.0
	$ pip install wsgiref==0.1.2 

## Project outline

#### Data directories

- `sample-xls-input` - contains example output from EJP SQL query  
- `sample-xml-generated-output` - place xml that our script generates into this directory
- `sample-xml-required-output` - contains the XML specification from production, our generated XML should match the format of the XML in this directory  

#### Python scripts

- `example-settings.py` gives an example configuration script. Copy this to `settings.py` and adjust for your own path structure.  
- `xml_generation.py` generates a set of xml files based on articles that we have published.  
- `generatePoaXml.py` set of classes for modelling the output XML.  
- `parseXlsFiles.py` reads data from provided XLS files, provides simple interface to the data.  

Other files in the repo are represent incomplete or earlier work.

#### Settings

Scripts look for file paths in a `settings.py` file. An example is provided in `example-settings.py`. Copy this example to `settings.py` and configure for
your own path structure. It will look for the following information:

	- `XLS_PATH` the location of the xls files to be read in.  
	- `TARGET_OUTPUT_DIR` a path to a directory for writing generated xml files.  
	- `XLS_FILES` a dict giving a label to the files that will be processed in the XLS read pahse.
	- `XLS_COLUMN_HEADINGS` a dict listing column heading names of interest in the XLS files that we will process.

#### Obtaining XLS fils to process

These files are generated out of the EJP system via a set of SQL queries. We do not store this data in this repository. Please contact @nathanlisgo to obtain a set for processing. We are currently procssing the following files. These files are versioned. The root of the filename gives an indication of what data we expect in these files. You should obtain the following files:

	poa_author_ : information about eLife authors  
	poa_license_ : licensing information for articles  
	poa_manuscript_ : manuscript details, including abstract and reviewing editor information  
	poa_received : recieved dates for manuscripts  
	poa_subject_area_ : information on subject areas for the manuscripts  
	organisms : information on organsisims that the manuscripts operate on  

Each of these files needs to be placed into the directory located at `XLS_PATH` in settings.py.

#### Generating XML from and XLS file

	$ python xml_generation.py

#### Verifying XML file

	$ xmllint --noout --loaddtd --valid sample-xml-generated-output/outputName.xml

## Project issues

Live code issues are listed as issues in the [git repo for this project](https://github.com/elifesciences/elife-poa-xml-generation/issues).

# Version history

2013-12-30 robust reviewed script ready.
2013-12-09 inital batch of code ready to review.
2013-11-26 first proof of concept.
