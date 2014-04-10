from ftplib import FTP
import settings as settings
import glob
import os

"""
Will deliver to the named HW ftp bucket.



## Gotchas

I noted that on one run with a large number of PDFs the upload speed
was very slow, might need to be investigated

# TODO - elife - imulvany - put in place a check to see that zip files contain all expected data
# TODO - elife - imulvany - find out the final location for FTP delivery

"""


source_dir = settings.FTP_TO_HW_DIR
ftpuri = settings.FTP_URI
ftpusername = settings.FTP_USERNAME
ftppassword = settings.FTP_PASSWORD
ftpcwd = settings.FTP_CWD


def upload(ftp, file):
	ext = os.path.splitext(file)[1]
	print file
	uploadname = file.split(os.sep)[-1]
	if ext in (".txt", ".htm", ".html"):
		ftp.storlines("STOR " + file, open(file))
	else:
		print "uploading " + uploadname
		ftp.storbinary("STOR " + uploadname, open(file, "rb"), 1024)
		print "uploaded " + uploadname

def ftp_to_endpoint(zipfiles):
	for zipfile in zipfiles:
		ftp = FTP(ftpuri, ftpusername, ftppassword)
		if ftpcwd != "":
			ftp.cwd(ftpcwd)
		upload(ftp, zipfile)
		ftp.quit()
	
if __name__ == "__main__":
	zipfiles = glob.glob(source_dir + "/*.zip")
	ftp_to_endpoint(zipfiles)
	workflow_logger.info("files uploaded to endpoint using ftp")

