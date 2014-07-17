"""
quickly zip some archives
"""

import os
import zipfile
import glob

def zip_matching_files(pdf_file_articles_numbers, xml_file_articles_numbers, zf):
	for file in pdf_file_articles_numbers:
		if file in xml_file_articles_numbers:
			absname = file + ".pdf"
			arcname = absname.split("/")[1]
			zf.write(absname, arcname)
			absname = file + ".xml"
			arcname = absname.split("/")[1]
			print absname, arcname
			zf.write(absname, arcname)

def zip_directory(dir, zipname):
	files = glob.glob(zip_target + "/*")
	for filename in files:
		arcname = filename.split("/")[-1]
		print filename
		print arcname
		zf.write(filename, arcname)

dir_root = "/Users/ian/Dropbox/code/public-code/forks/elife-poa-xml-generation-body/sample-zip-from-ejp/"

directories =  ["3067_1_supp_mat_highwire_zip_45156_n22sp5",
			    "3271_1_supp_mat_highwire_zip_45160_n22sgj",
				"3512_1_supp_mat_highwire_zip_45163_n22swd"]

for directory in directories:
	zip_target = dir_root + directory
	zip_name = directory + ".zip"
	zf = zipfile.ZipFile(zip_name, "w")
	files = glob.glob(zip_target + "/*")
	print zip_target, files
	zip_directory(zip_target, zf)
