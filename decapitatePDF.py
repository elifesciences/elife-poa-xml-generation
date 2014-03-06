from PyPDF2 import PdfFileWriter, PdfFileReader
import settings as settings
import glob
import logging

"""
This script uses the fact that the cover pages of pdfs provided
by EJP return no content when parsed by PyPDF2.

When extracting these pages and exracting their content, we get a null
value.

This means that we hope that the first page that returns a non null value will be the
first page of the author supplied manuscript.

We open the EJP pdf, we iterate over the first half dozen or so pages,
and we look for a match to "match_text" which is specified in a settings file.
At the moment we are matching against a page number - `3`.

About 7% of pdfs, in testing, could not be opened, or presented a problem, for this
script. In places where that happens we should email production@elifesciences.org

In addition, testing has shown that all cover pages, to date, have taken up no more
than 3 PDF pages, so if we find ourselves decapitating more than 3 pages, there is
probably a problem, and we should abort, and send an error message to production@elifesciecnes.org 

"""

logger = logging.getLogger("decapitator")
hdlr = logging.FileHandler("decapitator.log")
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.ERROR)

def initalise():
	logger.info("\n\ninialising")
	file_system = settings.FILE_SYSTEM
	if file_system == settings.LOCAL_INDICATOR:
		input_dir = settings.LOCAL_INPUT_DIR
		output_dir = settings.LOCAL_OUTPUT_DIR
	elif file_system == settings.AWS_INDICATOR:
		input_dir = settings.AWS_INPUT_DIR
		output_dir = settings.AWS_OUTPUT_DIR
	logger.info("opening files from " + input_dir)
	return input_dir

def get_match_text(override_match_text=None):
	"""
	the match text is used to determine if we are looking at an author proof pdf.
	At the moment pdfs from EJP do not render any content from the coverpages
	using the PyPDF lib.

	The default settings file uses `2` as the match text.
	"""
	logging.info("about to get match text")
	match_text = ""
	if override_match_text:
		match_text = override_match_text
	else:
		match_text = settings.MATCH_TEXT
	logging.info("match_text is "+ match_text)
	return match_text

def get_all_pdfs_aws():
	pass

def get_all_pdfs_local_file(input_dir):
	"""
	returns a list of local paths to pdfs that we want to examine.
	"""
	logger.info("about to get pdfs form local dir " + input_dir)
	pdfs = glob.glob(input_dir + "/*.pdf")
	logger.info(str(pdfs))
	return pdfs

def get_all_pdfs(input_dir, file_system):
	"""
	returns a list of all pdfs that we want to operate on
	TODO: comlpete support for aws filesystem
	"""
	logger.info("about to get all pdfs")
	if file_system == settings.LOCAL_INDICATOR:
		all_pdfs_list = get_all_pdfs_local_file(input_dir)
		return all_pdfs_list
	else:
		logger.error("no supported file system sypplied")

def setup_pdf_reader(input_pdf_path):
	input_pdfreader = PdfFileReader(open(input_pdf_path, "rb"))
	return input_pdfreader

def set_output_path(input_pdf_path, output_dir):
	logger.info(input_pdf_path + " " + output_dir)
	filename = input_pdf_path.split("/")[-1]
	output_pdf_path = output_dir + filename
	logger.info(output_pdf_path)
	return output_pdf_path

def setup_pdf_writer():
	output_pdfwriter = PdfFileWriter()
	return output_pdfwriter

def get_article_first_page(input_pdfreader, matchtext):
	start_pages = []
	pages = input_pdfreader.getNumPages()
	pagerange = range(pages)
	for page in pagerange[0:6]:  # we have hard coded the number of pages that we check for a match, mainly for convienience
		pdfPage = input_pdfreader.getPage(page)
		text = pdfPage.extractText()
		if text.find(matchtext) > -1: start_pages.append(page)
	start_page = start_pages[0]
	logger.info("start page is " + str(start_page))
	return start_page

def generate_headless_pdf(pdf_reader, start_page):
	headless_pdf = setup_pdf_writer()
	pages = pdf_reader.getNumPages()
	pagerange = range(pages)
	for page in pagerange[start_page:]:
		pdfPage = pdf_reader.getPage(page)
		headless_pdf.addPage(pdfPage)
	return headless_pdf

def write_headless_pdf(headless_pdf, pdf_input_path, output_dir):
	logger.info("getting output path")
	ouput_path = set_output_path(pdf_input_path, output_dir)
	logger.info("output path is " + output_dir)
	page_stream = file(ouput_path, "wb")
	headless_pdf.write(page_stream)

def decapitate_pdf(pdf_input_path, output_dir):
	match_text = get_match_text()
	pdf_reader = setup_pdf_reader(pdf_input_path)
	logger.info("setup pdf_reader")
	start_page = get_article_first_page(pdf_reader, match_text)
	logger.info("retreived start page")
	headless_pdf = generate_headless_pdf(pdf_reader, start_page)
	logger.info("generated headless pdf " + str(headless_pdf))
	write_headless_pdf(headless_pdf, pdf_input_path, output_dir)
	logger.info("wrote headless pdf")

if __name__ == "__main__":
	"""
	TODO: - elife - imulvany - clean up how we specify which file system we are operating from
	"""
	input_dir = initalise()
	file_system = settings.FILE_SYSTEM
	output_dir = settings.LOCAL_OUTPUT_DIR
	logger.info("file system is " + file_system)
	logger.info("output dir is " + output_dir)
	match_text = get_match_text()
	pdfs = get_all_pdfs(input_dir, file_system)
	for pdf in pdfs:
		logger.info("\n")
		logger.info("about to work on " + str(pdf))
		try:
			decapitate_pdf(pdf, output_dir)
			logger.info("decapitated " + pdf)
		except:
			logger.error("could not decapitate " + pdf)
