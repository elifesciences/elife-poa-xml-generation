import logging
import subprocess

logger = logging.getLogger("decapitator2")
hdlr = logging.FileHandler("decapitator2.log")
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

def decapitate_pdf_with_error_check(pdf_in, pdf_out):
    f = subprocess.Popen(["/opt/strip-coverletter/strip-coverletter.sh", pdf_in, pdf_out], \
                         stdout=subprocess.PIPE, \
                         stderr=subprocess.PIPE)
    stderr = f.stderr.read()
    stdout = f.stdout.read()

    print 'stderr'
    print stderr
    print
    print 'stdout'
    print stdout

if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    if len(args) < 2:
        print 'Usage: decapitatePDF2.py <pdf-in> <pdf-out>'
        exit(1)
    pin, pout = args[:2]
    decapitate_pdf_with_error_check(pin, pout)
