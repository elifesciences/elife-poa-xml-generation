import logging
import subprocess

FORMAT = logging.Formatter("%(created)f - %(levelname)s - %(processName)s - %(name)s - %(message)s")
LOGFILE = "decapitator2.log"

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

h = logging.FileHandler(LOGFILE)
h.setLevel(logging.INFO)
h.setFormatter(FORMAT)

logger.addHandler(h)

def decapitate_pdf_with_error_check(pdf_in, pdf_out_dir):
    # PDF out file name
    pdf_out = pdf_out_dir + pdf_in.split('/')[-1]
    
    f = subprocess.Popen(["/opt/strip-coverletter/strip-coverletter.sh", pdf_in, pdf_out], \
                         stdout=subprocess.PIPE, \
                         stderr=subprocess.PIPE)

    stderr = f.stderr.read()
    stdout = f.stdout.read()

    # subprocess.Popen doesn't interleave pipe output,
    # so neither will these log messages
    map(logger.info, stdout.splitlines())
    map(logger.error, stderr.splitlines())

    return stderr != '' # no errors

if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    if len(args) < 2:
        print 'Usage: decapitatePDF2.py <pdf-in> <pdf-out>'
        exit(1)
    
    h2 = logging.StreamHandler()
    h2.setLevel(logging.DEBUG)
    h2.setFormatter(FORMAT)
    logger.addHandler(h2)
    
    pin, pout = args[:2]
    decapitate_pdf_with_error_check(pin, pout)
