
[![Build Status](https://travis-ci.org/elifesciences/elife-poa-xml-generation.svg?branch=master)](https://travis-ci.org/elifesciences/elife-poa-xml-generation)

[![Coverage Status](https://coveralls.io/repos/elifesciences/elife-poa-xml-generation/badge.svg?branch=master&service=github)](https://coveralls.io/github/elifesciences/elife-poa-xml-generation)

# Background

This project creates JATS XML files for Publish on Accept (PoA) articles. It is centred around using a set of CSV data files as input, although an intermediary data object could be populated with data from other sources.

Also concerning the publication of PoA articles, it can transform the files in a zip package into the desired publishable format. It decapitates the cover page from a PDF file, and rezips other files into a new supplementary zip file.

The can also create CrossRef and PubMed deposits from an XML file input. An XML parser (``parsePoaXml.py``) can produce an article object using XML as the input (as opposed to from CSV data). From that article a CrossRef or PubMed batch deposit file is produced.

Examples of input and outbox can be found in the test cases.


## Installation

Create virtualenv, activate it and install required libraries
    `virtualenv -venv`
    `source venv/bin/activate`
    `pip install -r requirements.txt`

Copy the `exmple-settings.py` to a new file named `settings.py`.

You should be able to run the automated tests at this point.

## Configuration

### XML generation

To use the CSV data to article XML generation function, in the `settings.py` file you need to set the `XLS_PATH` to be the directory where the CSV files are stored. If you do not have any CSV files yet (and are just testing this project) there are sample CSV files in the automated tests you can use; in your `settings.py` file set it as
    `XLS_PATH = "tests/test_data/"`

Run the following and you should get some XML files produced in the `generated_xml_output` directory (the default output folder name)
    `python xml_generation.py`

### CrossRef and PubMed deposit generation

To test run the scripts `generateCrossrefXml.py` and `generatePubMedXml.py` at this time, edit the XML filenames in the `article_xmls[]` list at the bottom of the file when `__main__()` is run. You can also point these to some automated test data to try them out, for example, set it as

    `article_xmls = ["tests/test_data/elife-02935-v2.xml"]`

After running these scripts successfully, there should be new XML deposit files in the `tmp` directory.

### Others

There are some other functions, such as repackaging article zip files into a new format, decapitating PDF files, and some FTP transfer function, not documented here yet.

## Project dependencies

See `requirements.txt`.

## Testing

You can run the full automated test suite from the base folder with:

    `python -m unittest discover tests`

or you can run tests with coverage:

    `coverage run -m unittest discover tests`

and then view the coverage report:

    `coverage report -m`

# Copyright & Licence

Copyright 2016 eLife Sciences. Licensed under the [MIT license](LICENSE).

# Older readme notes below!

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

#### Obtaining XLS files to process

These files are generated out of the EJP system via a set of SQL queries. We do not store this data in this repository. Please contact @nathanlisgo to obtain a set for processing. We are currently procssing the following files. These files are versioned. The root of the filename gives an indication of what data we expect in these files. You should obtain the following files:

	poa_author_ : information about eLife authors  
	poa_license_ : licensing information for articles  
	poa_manuscript_ : manuscript details, including reviewing editor information  
	poa_received_ : recieved dates for manuscripts  
	poa_subject_area_ : information on subject areas for the manuscripts  
	poa_research_organism_ : information on organsisims that the manuscripts operate on
	poa_title_ : manuscript titles
	poa_abstract_ : manuscript abstracts

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

# Copyright & Licence

Copyright 2016 eLife Sciences. Licensed under the [MIT license](LICENSE).