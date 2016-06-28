import os

TEST_BASE_PATH = os.path.dirname(os.path.abspath(__file__)) + os.sep
TEST_TEMP_DIR = TEST_BASE_PATH + "tmp" + os.sep

# xls reading settings
ROWS_WITH_COLNAMES = 3
DATA_START_ROW = 4

XLS_PATH = TEST_BASE_PATH + "test_data" + os.sep


XLS_FILES = {
    "authors" : "poa_author.csv",
    "license" : "poa_license.csv",
    "manuscript" : "poa_manuscript.csv",
    "received" : "poa_received.csv",
    "subjects" : "poa_subject_area.csv",
    "organisms": "poa_research_organism.csv",
    "abstract" : "poa_abstract.csv",
    "title": "poa_title.csv",
    "keywords": "poa_keywords.csv",
    "group_authors": "poa_group_authors.csv",
    "datasets": "poa_datasets.csv"
            }

OVERFLOW_XLS_FILES = ["abstract", "title"]


XLS_COLUMN_HEADINGS = {
    "author_position" : "poa_a_seq",
    "subject_areas" : "poa_s_subjectarea",
    "license_id" : "poa_l_license_id",
    "title" : "poa_m_title_tag",
    "abstract" : "poa_m_abstract_tag",
    "doi" : "poa_m_doi",
    "articleType" : "poa_m_type",
    "accepted_date" : "poa_m_accepted_dt",
    "received_date" : "poa_r_received_dt",
    "receipt_date" : "poa_r_receipt_dt2",
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
    "organisms" : "poa_ro_researchorganism",
    "keywords" : "poa_kw_keyword",
    "group_author" : "poa_ga",
    "orcid" : "ORCID",
    "datasets" : "poa_m_dataset_note"
}

# xml writing settings
TARGET_OUTPUT_DIR = TEST_TEMP_DIR + "generated_xml_output"

STAGING_TO_HW_DIR = TEST_TEMP_DIR + "unpacked_renamed_ejp_files"
FTP_TO_HW_DIR = TEST_TEMP_DIR + "ftp-to-hw"
MADE_FTP_READY = TEST_TEMP_DIR + "made_ftp_ready_on"
EJP_INPUT_DIR = TEST_TEMP_DIR + "sample-zip-from-ejp"
STAGING_DECAPITATE_PDF_DIR = TEST_TEMP_DIR + "staging_decapitate_pdf_dir"
TMP_DIR = TEST_TEMP_DIR + "tmp"

MATCH_TEXT = `3`
#MATCH_TEXT = "Deaton"
#MATCH_TEXT = 'Introduction'

FTP_URI = ""
FTP_USERNAME = ""
FTP_PASSWORD = ""
FTP_CWD = ""



LESS_THAN_ESCAPE_SEQUENCE = 'LTLT'
GREATER_THAN_ESCAPE_SEQUENCE = 'GTGT'


