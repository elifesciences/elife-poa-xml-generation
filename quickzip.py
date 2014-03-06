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
directories =  ["1135_0_supp_mat_highwire_zip_00003",
				"1135_0_supp_mat_highwire_zip_00005",
				"1135_0_supp_mat_highwire_zip_00007",
				"1135_0_supp_mat_highwire_zip_00012",
				"1135_0_supp_mat_highwire_zip_00013",
				"1135_0_supp_mat_highwire_zip_00031",
				"1135_0_supp_mat_highwire_zip_00036",
				"1135_0_supp_mat_highwire_zip_00047"]

for directory in directories:
	zip_target = dir_root + directory
	zip_name = directory + ".zip"
	zf = zipfile.ZipFile(zip_name, "w")
	files = glob.glob(zip_target + "/*")
	print zip_target, files 
	zip_directory(zip_target, zf)