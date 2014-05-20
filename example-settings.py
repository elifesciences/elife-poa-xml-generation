
# xls reading settings
ROWS_WITH_COLNAMES = 3
DATA_START_ROW = 4

XLS_PATH = "/Users/ian/Dropbox/code/private-code/poa-xls-files/csv-input-v1.06/"




XLS_FILES = 	{"authors" : "ejp_query_tool_query_id_177_POA_Author_2014_02_12_eLife.csv",
				 "license" : "ejp_query_tool_query_id_178_POA_License_2014_02_12_eLife.csv",
				 "manuscript" : "ejp_query_tool_query_id_176_POA_Manuscript_2014_02_12_eLife.csv",
				 "received" : "ejp_query_tool_query_id_180_POA_Received_2014_02_12_eLife.csv",
				 "subjects" : "ejp_query_tool_query_id_179_POA_Subject_Area_2014_02_12_eLife.csv",
				 "organisms": "ejp_query_tool_query_id_182_POA_Research_Organism_2014_02_12_eLife.csv"}

XLS_COLUMN_HEADINGS = {"author_position" : "poa_a_seq",
					"subject_areas" : "poa_s_subjectarea",
					"license_id" : "poa_l_license_id",
					"title" : "poa_m_title",
					"abstract" : "poa_m_abstract",
					"doi" : "poa_m_doi",
					"accepted_date" : "poa_m_accepted_dt",
					"received_date" : "poa_r_received_dt",
					"editor_id" : "poa_m_me_id",
					"editor_last_name" : "poa_m_me_last_nm",
					"editor_first_name" : "poa_m_me_first_nm",
					"editor_middle_name" : "poa_m_me_middle_nm",
					"editor_institution" : "poa_m_me_organization",
					"editor_department" : "poa_m_me_department",
					"editor_country" : "poa_m_me_country",
					"ethics" : "poa_m_ethics_note",
					"author_id" : "poa_a_id",
					"email" : "poa_a_email",
					"author_type" : "poa_a_type_cde",
					"dual_corresponding" : "poa_a_dual_corr",
					"author_last_name": "poa_a_last_nm",
					"author_first_name": "poa_a_first_nm",
					"author_middle_name" : "poa_a_middle_nm",
					"author_institution" : "poa_a_organization",
					"author_department" : "poa_a_department",
					"author_city" : "poa_a_city",
					"author_country" : "poa_a_country",
					"author_state" : "poa_a_state",
					"author_conflict" : "poa_a_cmp",
					"organisms" : "poa_ro_researchorganism"
				}

# xml writing settings
TARGET_OUTPUT_DIR = "generated_xml_output"

STAGING_TO_HW_DIR = "unpacked_renamed_ejp_files"
FTP_TO_HW_DIR = "ftp-to-hw"
MADE_FTP_READY = "made_ftp_ready_on"
EJP_INPUT_DIR = "sample-zip-from-ejp"
STAGING_DECAPITATE_PDF_DIR = "staging_decapitate_pdf_dir"
TMP_DIR = "tmp"

MATCH_TEXT = `3`

FTP_URI = ""
FTP_USERNAME = ""
FTP_PASSWORD = ""
FTP_CWD = ""
