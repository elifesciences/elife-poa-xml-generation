import zipfile
import glob
from xml.etree import ElementTree as ET
import logging
import settings as settings
import arrow
import xml
from xml.dom.minidom import Document
from collections import namedtuple
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom
import time
import re
from git import *
import settings
import os
import shutil
from func_timeout import func_timeout, FunctionTimedOut
#from decapitatePDF import decapitate_pdf_with_error_check
from decapitatePDF2 import decapitate_pdf_with_error_check

"""
open the zip file from EJP,

get the manifext.xml file

move the pdf to the hw staging dir

rename and move supp files to a new zipfile called
	elife_poa_e000213_supporting_files.zip

find the pdf file and move this to the hw ftp staging directory

generate a new manifest and instert into the new zip file

move the new zip file to the HW staging site

move the old ejp zip file to the processed files directory
"""

# local logger
logger = logging.getLogger('transformEjpToHWZip')
hdlr = logging.FileHandler('transformEjpToHWZip.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

# global logger
workflow_logger = logging.getLogger('ejp_to_hw_workflow')
hdlr = logging.FileHandler('ejp_to_hw_workflow.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
workflow_logger.addHandler(hdlr)
workflow_logger.setLevel(logging.INFO)

input_dir = settings.EJP_INPUT_DIR
output_dir = settings.STAGING_TO_HW_DIR
hw_ftp_dir = settings.FTP_TO_HW_DIR
tmp_dir = settings.TMP_DIR
decap_dir = settings.STAGING_DECAPITATE_PDF_DIR
PDF_DECAPITATE_TIMEOUT = 120

class manifestXML(object):

	def __init__(self, doi, new_zipfile):
		"""
		set the root node
		get the article type from the object passed in to the class
		set default values for items that are boilder plate for this XML
		"""

		self.root = Element('datasupp')
		self.root.set("sitecode", "elife")
		self.resource = SubElement(self.root, "resource")
		self.resource.set("type", "doi")
		self.resource.text = str(doi)

		self.linktext = SubElement(self.root, "linktext")
		self.linktext.text = "Supplementary data"
		
		# Add file elements to the manifest
		self.simple_manifest(new_zipfile, doi)

	def extended_manifest(self, new_zipfile):
		"""
		Old procedure to build a manifest XML based on the filenames
		found in the zip file
		"""
		filelist = new_zipfile.namelist()
		for filename in filelist:
			self.file = SubElement(self.root, "file")
			self.filename = SubElement(self.file, "filename")
			self.filename.text = filename

			self.title = SubElement(self.file, "title")
			self.title.text = filename

			self.description = SubElement(self.file, "description")
			self.description.text = filename
			
	def simple_manifest(self, new_zipfile, doi):
		"""
		Add a simple XML file element to the manifest
		Note: linktext element must come before title (order matters)
		"""
		# Filename is the folder inside the zip file
		filename_text = get_new_internal_zipfile_name(doi)
		linktext_text = "Download zip folder"
		title_text = "Any figures and tables for this article are included in the PDF."
		title_text += " The zip folder contains additional supplemental files."
		#title_text += self.get_file_contents_description(new_zipfile)
		
		# Add XML
		self.file = SubElement(self.root, "file")
		self.filename = SubElement(self.file, "filename")
		self.filename.text = filename_text

		self.description = SubElement(self.file, "linktext")
		self.description.text = linktext_text

		self.title = SubElement(self.file, "title")
		self.title.text = title_text
		
	def get_file_contents_description(self, new_zipfile):
		"""
		Given a zipfile, concatenate a description of the
		types of files inside
		"""
		file_count = 0
		extension_counts = {}
		description = ""
		filelist = new_zipfile.namelist()
		for filename in filelist:
			file_count = file_count + 1
			# Get the file extension
			try:
				extension = filename.split(".")[-1]
			except:
				extension = None
			# Increment count of the extension type
			try:
				extension_counts[extension] += 1
			except:
				# Create the extension if it does not exist yet in the counter
				extension_counts[extension] = 1
			
		description = description + " The zip folder contains " + str(file_count) + " files"
		if len(extension_counts) > 0:
			description = description + " including: "
			delim = ""
			for k,v in extension_counts.items():
				description = description + delim + "%s %s" % (v, k)
				delim = ", "
		description = description + "."
		
		return description
		


# self.department = SubElement(self.addline, "named-content")
# self.department.set("content-type", "department")
# self.department.text = affiliation.department
# self.addline.tail = ", "

		# set a comment
		generated = time.strftime("%Y-%m-%d %H:%M:%S")
		last_commit = get_last_commit_to_master()
		comment = Comment('generated by eLife at ' + generated + ' from version ' + last_commit)
		self.root.append(comment)

	def prettyXML(self):
		publicId = '-//HIGHWIRE//DTD HighWire Data Supplement Manifest//EN'
		systemId = 'http://schema.highwire.org/public/hwx/ds/datasupplement_manifest.dtd'
		encoding = 'ISO-8859-1'
		namespaceURI = None
		qualifiedName = "datasupp"

		doctype = ElifeDocumentType(qualifiedName)
		doctype._identified_mixin_init(publicId, systemId)

		rough_string = ElementTree.tostring(self.root, encoding)
		reparsed = minidom.parseString(rough_string)
		if doctype:
		    reparsed.insertBefore(doctype, reparsed.documentElement)
		return reparsed.toprettyxml(indent="\t", encoding = encoding)

class ElifeDocumentType(minidom.DocumentType):
	"""
	Override minidom.DocumentType in order to get
	double quotes in the DOCTYPE rather than single quotes
	"""
	def writexml(self, writer, indent="", addindent="", newl=""):
		writer.write("<!DOCTYPE ")
		writer.write(self.name)
		if self.publicId:
			writer.write('%s  PUBLIC "%s"%s  "%s"'
						 % (newl, self.publicId, newl, self.systemId))
		elif self.systemId:
			writer.write('%s  SYSTEM "%s"' % (newl, self.systemId))
		if self.internalSubset is not None:
			writer.write(" [")
			writer.write(self.internalSubset)
			writer.write("]")
		writer.write(">"+newl)

def get_last_commit_to_master():
    """
    returns the last commit on the master branch. It would be more ideal to get the commit
    from the branch we are currently on, but as this is a check mostly to help
    with production issues, returning the commit from master will be sufficient.
    """
    repo = Repo(".")
    last_commit = None
    try:
        last_commit = repo.commits()[0] 
    except AttributeError:
        # Optimised for version 0.3.2.RC1
        last_commit = repo.head.commit
    return str(last_commit)
    # commit =  repo.heads[0].commit
    # return str(commit)

def article_id_from_doi(doi):
	article_id = doi.split("/")[1]
	article_id = article_id.replace(".","")
	article_id = article_id.replace("eLife","e")
	return article_id

def get_datestamp():
	a = arrow.utcnow()
	date_stamp = str(a.datetime.year) + str(a.datetime.month).zfill(2) + str(a.datetime.day).zfill(2)
	return date_stamp

def gen_new_name_for_file(name, title, doi):
	"""
	take the following:
	and generates a file name like:
	"""
	file_ext = name.split(".")[1]
	article_id = article_id_from_doi(doi)
	new_name_front = title.replace(" ", "_")
	new_name_front = new_name_front.replace("-", "_")
	new_name_front = new_name_front.replace("__", "_")
	new_name_front = new_name_front.replace("__", "_")
	if new_name_front == "Merged_PDF":  # we ignore the main file name and just use our base POA convention
		new_name = "elife_poa_" + article_id + "." + file_ext
	else:
		new_name = "elife_poa_" + article_id + "_" + new_name_front + "." + file_ext
	return new_name

def get_doi_from_zipfile(ejp_input_zipfile):
	#print ejp_input_zipfile.namelist()
	manifest = ejp_input_zipfile.read("manifest.xml")
	tree = ET.fromstring(manifest)
	for child in tree:
		if child.tag == "resource":
			if child.attrib["type"] == "doi":
				doi = child.text
			elif child.attrib["type"] == "resourceid":
				doi_base = "10.7554/eLife."
				article_number = child.text.split("-")[-1]
				doi = doi_base + article_number
	return doi

def get_filename_new_title_map_from_zipfile(ejp_input_zipfile):
	workflow_logger.info("unpacking and renaming" + str(ejp_input_zipfile))
	file_title_map = {}
	manifest = ejp_input_zipfile.read("manifest.xml")
	tree = ET.fromstring(manifest)
	for child in tree:
		if child.tag == "file":
			for file in child:
				if file.tag == "filename": filename = file.text
				if file.tag == "title": title =  file.text
			file_title_map[filename] = title
	return file_title_map

# def unpack_and_rename_files_from_zip(ejp_input_zipfile):
# 	print ejp_input_zipfile
# 	if doi:
# 		zf = zipfile.ZipFile(ejp_input_zipfile, 'r')
# 		logger.info("doi obtained for " + str(ejp_input_zipfile))
# 		for name in file_title_map.keys():
# 			title = file_title_map[name]
# 			new_name = gen_new_name_for_file(name, title, doi)
# 			file = zf.read(name)
# 			out_handler = open(output_dir + "/" + new_name, "w")
# 			out_handler.write(file)
# 			out_handler.close()
# 			print new_name
# 	else:
# 		logger.warning("unable to find a doi for " + str(ejp_input_zipfile))

def get_new_zipfile_name(doi):
	article_id = article_id_from_doi(doi)
	new_zipfile_name = "elife_poa_" + article_id + "_ds.zip"
	return new_zipfile_name

def get_new_internal_zipfile_name(doi):
	article_id = article_id_from_doi(doi)
	# Remove the leading 'e' from article_id
	doi_id = article_id[1:]
	new_zipfile_folder_name = "elife" + doi_id + "_Supplemental_files.zip"
	return new_zipfile_folder_name

def gen_new_internal_zipfile(doi):
	new_zipfile_name = get_new_internal_zipfile_name(doi)
	new_zipfile_name_plus_path = tmp_dir + "/" + new_zipfile_name
	new_zipfile = zipfile.ZipFile(new_zipfile_name_plus_path, 'w')
	return new_zipfile

def gen_new_zipfile(doi):
	new_zipfile_name = get_new_zipfile_name(doi)
	new_zipfile_name_plus_path = tmp_dir + "/" + new_zipfile_name
	new_zipfile = zipfile.ZipFile(new_zipfile_name_plus_path, 'w')
	return new_zipfile

def move_files_into_new_zipfile(current_zipfile, file_title_map, new_zipfile, doi):
	for name in file_title_map.keys():
		title = file_title_map[name]
		new_name = gen_new_name_for_file(name, title, doi)

		file = current_zipfile.read(name)
		temp_file_name = tmp_dir + "/" + "temp_transfer"
		f = open(temp_file_name, "wb")
		f.write(file)
		f.close()
		new_zipfile.write(temp_file_name, new_name)

def add_file_to_zipfile(new_zipfile, name, new_name = None):
	"""
	Simple add a file to a zip file
	"""
	if not new_name:
		new_name = name
		
	new_zipfile.write(name, new_name)

def alert_production(alert_message):
	""
	test_message = "holy shit batman, something's gone wrong"

def copy_pdf_to_hw_staging_dir(file_title_map, output_dir, doi, current_zipfile):
	"""
	we will attempt to generate a headless pdf and move this pdf
	to the ftp staging site.

	if this headless creation fails, we will raise an error to
	production@elifesciecnes.org, and try to copy the original pdf
	file to ftp staging

	the function that we call to decapitate the pdf is contained in decapitatePDF.py.
	It manages some error handline, and tries to determine witheher the pdf
	cover content has been celanly removed.

	TODO: - elife - ianm - tidy up paths to temporary pdf decpitation paths
	"""


	for name in file_title_map.keys():
		# we extract the pdf from the zipfile
		title = file_title_map[name]

		if title == "Merged PDF":
			print title
			new_name = gen_new_name_for_file(name, title, doi)
			file = current_zipfile.read(name)
			print new_name
			decap_name = "decap_" + new_name
			decap_name_plus_path = tmp_dir + "/" + decap_name
			# we save the pdf to a local file
			temp_file = open(decap_name_plus_path, "wb")
			temp_file.write(file)
			temp_file.close()

	decap_status = None
	try:
		# pass the local file path, and the path to a temp dir, to the decapitation script
		decap_status = func_timeout(
			PDF_DECAPITATE_TIMEOUT, decapitate_pdf_with_error_check, args=(
				decap_name_plus_path, decap_dir + "/"))
	except FunctionTimedOut:
		decap_status = False
		timeout_message = "PDF decap did not finish within {x} seconds".format(x=PDF_DECAPITATE_TIMEOUT)
		logger.error(timeout_message)

	if decap_status:
		# pass the local file path, and teh path to a temp dir, to the decapiation script
		try:
			move_file = open(decap_dir + "/" + decap_name, "rb").read()
			out_handler = open(output_dir + "/" + new_name, "wb")
			out_handler.write(move_file)
			out_handler.close()
			print "decapitaiton worked"
		except:
			# The decap may return true but the file does not exist for some reason
			#  allow the transformation to continue in order to processes the supplementary files
			alert_message = "decap returned true but the pdf file is missing " + new_name
			logger.error(alert_message)
	else:
		# if the decapitation script has failed, we move the original pdf file
		move_file = file
		alert_message = "could not decapitate " + new_name
		logger.error(alert_message)
		alert_production(alert_message)


def remove_pdf_from_file_title_map(file_title_map):
	new_map = {}
	for name in file_title_map.keys():
		title = file_title_map[name]
		if title == "Merged PDF":
			continue
		else:
			new_map[name] = title
	return new_map

def generate_hw_manifest(new_zipfile, doi):
	manifestObject = manifestXML(doi, new_zipfile)
	manifest = manifestObject.prettyXML()
	return manifest

def move_new_zipfile(doi, hw_ftp_dir):
	new_zipfile_name = get_new_zipfile_name(doi)
	new_zipfile_name_plus_path = tmp_dir + "/" + new_zipfile_name
	shutil.move(new_zipfile_name_plus_path, hw_ftp_dir + "/" + new_zipfile_name)

def add_hw_manifest_to_new_zipfile(new_zipfile, hw_manifest):
	temp_file_name = tmp_dir + "/" + "temp_transfer"
	f = open(temp_file_name, "w")
	f.write(hw_manifest)
	f.close()
	new_zipfile.write(temp_file_name, "manifest.xml")

def get_doi_from_zipfile_name(current_zipfile):
	"""
	function is introduced to deal with lack of DOI
	being provided by EJP. We infer the article number
	from the name of the zip file, and we generate
	a doi off of this.

	Other code that takes the doi as an argument requires a full doi
	even though that code just uses this to parse backwards to the
	article number.

	TODO - elife - ianm - refactor code to use only article number
	"""
	doi_base = "10.7554/eLife."
	article_number = current_zipfile.split("_")[0]
	doi = doi_base + article_number
	return doi

def extract_pdf_from_zipfile(current_zipfile):
	pdf = "this is a pdf"
	return pdf

def process_zipfile(zipfile_name, output_dir):
	current_zipfile = zipfile.ZipFile(zipfile_name, 'r')
	doi = get_doi_from_zipfile(current_zipfile)
	#doi = get_doi_from_zipfile_name(zipfile_name)
	file_title_map = get_filename_new_title_map_from_zipfile(current_zipfile)
	#extracted_pdf = extract_pdf_from_zipfile(current_zipfile)
	copy_pdf_to_hw_staging_dir(file_title_map, output_dir, doi, current_zipfile)
	pdfless_file_title_map = remove_pdf_from_file_title_map(file_title_map)
	
	# Internal zip file
	internal_zipfile = gen_new_internal_zipfile(doi)
	move_files_into_new_zipfile(current_zipfile, pdfless_file_title_map, internal_zipfile, doi)
	internal_zipfile.close()
	
	# Outside wrapping zip file
	new_zipfile = gen_new_zipfile(doi)
	new_name = internal_zipfile.filename.split("/")[-1]
	add_file_to_zipfile(new_zipfile, internal_zipfile.filename, new_name)
	
	hw_manifest = generate_hw_manifest(new_zipfile, doi)
	add_hw_manifest_to_new_zipfile(new_zipfile, hw_manifest)
	# Close zip file before moving
	new_zipfile.close()
	move_new_zipfile(doi, hw_ftp_dir)

if __name__ == "__main__":
	input_dir = settings.EJP_INPUT_DIR
	output_dir = settings.STAGING_TO_HW_DIR
	files = glob.glob(input_dir + "/*.zip")
	for input_zipfile in files:
		logger.info("\n\n")
		logger.info("working on " + input_zipfile)
		process_zipfile(input_zipfile, output_dir)
