from ftplib import FTP
import settings as settings
import glob
import os

"""
Will deliver to the named HW ftp bucket.



## Gotchas

I noted that on one run with a large number of PDFs the upload speed
was very slow, might need to be investigated

# TODO - elife - imulvany - find out the final location for FTP delivery

"""


source_dir = settings.FTP_TO_HW_DIR
ftpuri = settings.FTP_URI
ftpusername = settings.FTP_USERNAME
ftppassword = settings.FTP_PASSWORD

zipfiles = glob.glob(source_dir + "/*.zip")


def upload(ftp, file):
	ext = os.path.splitext(file)[1]
	print file
	uploadname = file.split("/")[1]
	if ext in (".txt", ".htm", ".html"):
		ftp.storlines("STOR " + file, open(file))
	else:
		print "uploading " + uploadname
		ftp.storbinary("STOR " + uploadname, open(file, "rb"), 1024)
		print "uploaded " + uploadname

for zipfile in zipfiles:
	ftp = FTP(ftpuri, ftpusername, ftppassword)
	upload(ftp, zipfile)
	ftp.quit()
