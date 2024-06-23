'''Module to Model definition for the BrainNet Graph'''
from enum import Enum
import graphdb.cypher as cypher
import config.includes as includes


# Enumerations for the model
class NodeType(Enum):
    '''Model Node type enumeration'''
    def __init__(self, label, load,modelpath,arraykey):
        self.label = label
        self.load = load
        self.modelpath = modelpath
        self.arraykey = arraykey

    # Topology nodes

    BRAINREG='BRAINREG', cypher.LOAD_BRAINREG, includes.MODEL_JSON_NODES + "/brainregion.json", 'brainregions'
    CHANNEL='CHANNEL', cypher.LOAD_CHANNEL, includes.MODEL_JSON_NODES + "/channel.json", 'channels'
    
    # EEG Data Set nodes
    READS='READ', cypher.LOAD_READ, includes.MODEL_JSON_NODES + "/read.json", 'reads'
    SUBJECT='SUBJ', cypher.LOAD_SUBJECT, includes.MODEL_JSON_NODES + "/subject.json", 'subjects'
    ALPHA='ALPHA', cypher.LOAD_ALPHA, includes.MODEL_JSON_NODES + "/alpha_power.json", 'alpha_powers'
    BETA='BETA', cypher.LOAD_BETA, includes.MODEL_JSON_NODES + "/beta_powers.json", 'beta_powers'
    THETA='THETA', cypher.LOAD_THETA, includes.MODEL_JSON_NODES + "/theta_power.json", 'theta_powers'
    DELTA='DELTA', cypher.LOAD_BETA, includes.MODEL_JSON_NODES + "/delta_power.json", 'delta_powers'
    GAMMA='GAMMA', cypher.LOAD_GAMMA, includes.MODEL_JSON_NODES + "/gamma_power.json", 'gamma_powers'

class RelationType(Enum):
    '''Model relation type enumeration'''
    def __init__(self, label, load, modelpath, arraykey, birectional=False):
        self.label = label
        self.load = load
        self.modelpath = modelpath
        self.arraykey = arraykey
        self.birectional = birectional

    # Directed relations

    # Topology relations
    LOC_AT='LOC_AT',  cypher.LOAD_LOCATED_AT, includes.MODEL_JSON_RELATIONS + "/loc_at.json", 'channels_at_location', True
    CHAIN_NEXT='CHAIN_NEXT',  cypher.LOAD_CHAIN, includes.MODEL_JSON_RELATIONS + "/chain_next.json", 'chain_next', True

    # EEG Data Set relations
    READ_FOR='READ_FOR', cypher.LOAD_READ_FOR, includes.MODEL_JSON_RELATIONS + "/read_for.json", 'reads_for_subject', True
    READ_AT='READ_AT',  cypher.LOAD_READ_AT, includes.MODEL_JSON_RELATIONS + "/read_at.json", 'reads_at_channel', True
    ABS_POWER='ABS_POWER',  cypher.LOAD_ABSOLUTE_POWER, includes.MODEL_JSON_RELATIONS + "/absolute_power.json", 'reads_absolute_power', True

