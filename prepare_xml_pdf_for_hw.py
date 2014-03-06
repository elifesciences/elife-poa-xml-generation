import glob
import settings as settings
import zipfile 
import arrow
import os 
import shutil

"""
look in unpacked_renamed_ejp_files

look for all matching pdf and xml files 
	elife_poa_e000213.xml
	elife_poa_e000213.pdf 

If there is an xml or pdf file that is not matched, log an error

for the day of delivery take these files and put them into a zip file named
	elife_poa_YYYYMMDD.zip

put that zip file into `ftp-to-hw`

move processed pdf and xml files into
	made_ftp_ready_on/YYYMMDD  


GOTCHAS
When run multiple times it may possibly corrupt exising zip files, worthy of investigation. 

"""

def zip(src, dst):
    zf = zipfile.ZipFile("%s.zip" % (dst), "w")
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print 'zipping %s as %s' % (os.path.join(dirname, filename),
                                        arcname)
            zf.write(absname, arcname)
    zf.close()

# zip("src", "dst")

def check_matching_files_exist(pdf_file_articles_numbers, xml_file_articles_numbers):
	for file in pdf_file_articles_numbers:
		if file not in xml_file_articles_numbers: print file, " has no xml match"

	for file in xml_file_articles_numbers:
		if file not in pdf_file_articles_numbers: print file, " has no pdf match"

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

def move_zipfile_to_hw_staging(xml_pdf_zip, ftp_to_hw):
	shutil.move(xml_pdf_zip, ftp_to_hw + "/" + xml_pdf_zip)

def move_processed_files(pdf_file_articles_numbers, xml_file_articles_numbers, sourcedir, made_ftp_ready):
	for file in pdf_file_articles_numbers:
		if file in xml_file_articles_numbers:
			absname = file + ".pdf"
			arcname = absname.split("/")[1]
			print absname
			print arcname
			shutil.move(sourcedir + "/" + arcname, made_ftp_ready + "/" + arcname)
			absname = file + ".xml"
			arcname = absname.split("/")[1]			
			shutil.move(sourcedir + "/" + arcname, made_ftp_ready + "/" + arcname)

sourcedir = settings.STAGING_TO_HW_DIR
ftp_to_hw = settings.FTP_TO_HW_DIR

pdf_files = glob.glob(sourcedir + "/*.pdf")
xml_files = glob.glob(sourcedir + "/*.xml")

pdf_file_articles_numbers = []
xml_file_articles_numbers = []
for f in pdf_files: pdf_file_articles_numbers.append(f.split(".pdf")[0])
for f in xml_files: xml_file_articles_numbers.append(f.split(".xml")[0])

a = arrow.utcnow() 
print str(a.datetime.year)
print str(a.datetime.month).zfill(2)
print str(a.datetime.day).zfill(2)

date_stamp = str(a.datetime.year) + str(a.datetime.month).zfill(2) + str(a.datetime.day).zfill(2)

xml_pdf_zip = "elife_poa_" + date_stamp + ".zip"
made_ftp_ready = settings.MADE_FTP_READY

made_ftp_ready_dir = made_ftp_ready + "/" + date_stamp
if not os.path.exists(made_ftp_ready_dir):
    os.makedirs(made_ftp_ready_dir)

zf = zipfile.ZipFile(xml_pdf_zip, "w")
check_matching_files_exist(pdf_file_articles_numbers, xml_file_articles_numbers)
zip_matching_files(pdf_file_articles_numbers, xml_file_articles_numbers, zf)
move_zipfile_to_hw_staging(xml_pdf_zip, ftp_to_hw)
move_processed_files(pdf_file_articles_numbers, xml_file_articles_numbers, sourcedir, made_ftp_ready_dir)

