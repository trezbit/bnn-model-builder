'''Module to define constants and config functions for the project'''
import os
from pathlib import Path
from enum import Enum
import configparser


ROOT_DIR = os.path.abspath(Path(__file__).parent.parent)

# Corpus, mappings, samples
MODEL_EEGDATA_BASE= ROOT_DIR + "/data/eeg"

# Model IO files
MODEL_BASE= ROOT_DIR + "/graphdb"
MODEL_JSON_NODES= MODEL_BASE + "/nodes"
MODEL_JSON_RELATIONS= MODEL_BASE + "/edges"
MODEL_CSV_BASE= MODEL_BASE + "/csv"



# Graph data public sets -- for cloud graph db access
PUBLIC_GRAPH_DATA_ROOT = "https://raw.githubusercontent.com/trezbit/bnn-model-builder/master/graphdb/csv"
