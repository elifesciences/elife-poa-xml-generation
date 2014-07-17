from ftplib import FTP
import ftplib
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

def ftp_cwd_mkd(ftp, sub_dir):
	"""
	Given an FTP connection and a sub_dir name
	try to cwd to the directory. If the directory
	does not exist, create it, then cwd again
	"""
	cwd_success = None
	try:
		ftp.cwd(sub_dir)
		cwd_success = True
	except ftplib.error_perm:
		# Directory probably does not exist, create it
		ftp.mkd(sub_dir)
		cwd_success = False
	if cwd_success is not True:
		ftp.cwd(sub_dir)
		
	return cwd_success

def ftp_to_endpoint(zipfiles, sub_dir = None):
	for zipfile in zipfiles:
		ftp = FTP(ftpuri, ftpusername, ftppassword)
		ftp_cwd_mkd(ftp, "/")
		if ftpcwd != "":
			ftp_cwd_mkd(ftp, ftpcwd)
		if sub_dir is not None:
			ftp_cwd_mkd(ftp, sub_dir)
		
		upload(ftp, zipfile)
		ftp.quit()
	
if __name__ == "__main__":
	zipfiles = glob.glob(source_dir + "/*.zip")
	ftp_to_endpoint(zipfiles)
	workflow_logger.info("files uploaded to endpoint using ftp")

