# EJP to Highwire Workflow - quickstart.

Files come in to `sample-zip-from-ejp/`. When a zip file arrives into this
location then  

	$ python transform-ejp-zip-to-hw-zip.py`  

This populates `unpacked_renamed_ejp_files/` with the pdf sent from EJP. It also places
the newly minted supplementary zipfile into `fpt-to-hw`. At this point we need
to figure out how to generate the associated PAO XML file for the pdf that has bee
delivered into ``unpacked_renamed_ejp_files/`. Once that has been done you can then run

	$ python `prepare_xml_pdf_for_hw.py`

This will wrap the pdf and xml files for delivery into `ftp-to-hw`. You can then finally
run

	$ python ftp_to_highwire.py  


# EJP to Highwire Workflow - detailed description.

A zipfile arrives from EJP into the directory `sample-zip-from-ejp/`. The zipfile contains supporting material and a `manifest.xml`.
The `manifest.xml` contains a DOI.

We run `transform-ejp-zip-to-hw-zip.py`, it does the following

	gets a list of zipfiles from `sample-zip-from-ejp/`.

	For each zip file it extracts the doi contained within the `manifest.xml`

	map the file name to the file title, where the filename and title are in the manifest.xml

	find the pdf file in the zip file and rename and copy it to STAGING_TO_HW_DIR (in our case `unpacked_renamed_ejp_files/`).

	the pdf file is renamed to the pattern `elife_poa_e` + `stem of doi` + ".pdf".

	then we remove the pdf file from the title file map

	we create a new zip file named based off of the doi

	we copy the non pdf files into the new zip file, while renaming them based on their title and the doi.

	we create a new manifest file

	we add the manifest file into the zip file

	we finally move the new zip file into the directory FTP_TO_HW_DIR, which in our case is `ftp-to-hw`


This ends us up with the zipfile and manifest that need to be sent to HW with the supp files, but we still need to
wait on the generation of the POA xml, and matching this POA xml to the POA pdf.

In order to prepare this we run `prepare_xml_pdf_for_hw.py`.

This will do the following:

look in `unpacked_renamed_ejp_files`

look for all matching pdf and xml files
	elife_poa_e000213.xml
	elife_poa_e000213.pdf

If there is an xml or pdf file that is not matched, log an error

for the day of delivery take these files and put them into a zip file named
	elife_poa_YYYYMMDD.zip

put that zip file into `ftp-to-hw`

move processed pdf and xml files into
	made_ftp_ready_on/YYYMMDD  

## Helper functions

`quickzip.py` is a function that quickly generates a set of zip files for testing the workflow with.
