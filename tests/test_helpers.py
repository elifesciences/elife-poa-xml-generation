import os
import parseCSVFiles
import generatePoaXml
import xml_generation

# Import test settings last in order to override the regular settings
import poa_test_settings

def override_settings():
    # For now need to override settings to use test data
    xml_generation.settings = poa_test_settings
    parseCSVFiles.settings = poa_test_settings
    parseCSVFiles.XLS_PATH = poa_test_settings.XLS_PATH
    generatePoaXml.settings = poa_test_settings

def create_test_directories():
    for dir_name in [poa_test_settings.TEST_TEMP_DIR,
                     poa_test_settings.TARGET_OUTPUT_DIR,
                     poa_test_settings.TMP_DIR]:
        try:
            os.mkdir(dir_name)
        except OSError:
            pass
