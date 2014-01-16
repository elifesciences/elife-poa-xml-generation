
# xls reading settings 
ROWS_WITH_COLNAMES = 3
DATA_START_ROW = 4
XLS_PATH = "/Users/ian/Dropbox/code/private-code/poa-xls-files/ejp_queries_v1.04/" 

XLS_FILES = 	{"authors" : "poa_author_v1.04.xls",
				 "license" : "poa_license_v1.04.xls",
				 "manuscript" : "poa_manuscript_v1.04.xls",
				 "received" : "poa_received.04.xls",
				 "subjects" : "poa_subject_area_v1.04.xls",
				 "organisms": "poa_research_organism_v1.04.xls"}

XLS_COLUMN_HEADINGS = {"author_position" : "poa_a_seq",
					"subject_areas" : "poa_s_subjectarea",
					"license_id" : "poa_l_license_id",
					"title" : "poa_m_title",
					"abstract" : "poa_m_abstract",
					"doi" : "poa_m_doi",
					"accepted_date" : "poa_m_accepted_dt",
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
TARGET_OUTPUT_DIR = "generated_xml_output/"