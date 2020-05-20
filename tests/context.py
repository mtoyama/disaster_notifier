import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import src

data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
TEST_CONFIG_JSON = os.path.join(data_folder, 'test_config.json')
TEST_USGS_JSON = os.path.join(data_folder, 'test_usgs.json')