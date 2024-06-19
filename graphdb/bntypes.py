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

    SIDE='SIDE', cypher.LOAD_SIDE, includes.MODEL_JSON_NODES + "/sides.json", 'sides'
    LOBE='LOBE', cypher.LOAD_LOBE, includes.MODEL_JSON_NODES + "/lobes.json", 'lobes'
    CHANNEL='CHAN', cypher.LOAD_CHANNEL, includes.MODEL_JSON_NODES + "/channels.json", 'channels'
    READS='READ', cypher.LOAD_READ, includes.MODEL_JSON_NODES + "/reads.json", 'reads'
    SUBJECT='SUBJ', cypher.LOAD_SUBJECT, includes.MODEL_JSON_NODES + "/subjects.json", 'subjects'
    ALPHA='ALPHA', cypher.LOAD_ALPHA, includes.MODEL_JSON_NODES + "/alpha_powers.json", 'alpha_powers'
    BETA='BETA', cypher.LOAD_BETA, includes.MODEL_JSON_NODES + "/beta_powers.json", 'beta_powers'
    THETA='THETA', cypher.LOAD_THETA, includes.MODEL_JSON_NODES + "/theta_powers.json", 'theta_powers'
    DELTA='DELTA', cypher.LOAD_BETA, includes.MODEL_JSON_NODES + "/delta_powers.json", 'delta_powers'
    GAMMA='GAMMA', cypher.LOAD_GAMMA, includes.MODEL_JSON_NODES + "/gamma_powers.json", 'gamma_powers'

class RelationType(Enum):
    '''Model relation type enumeration'''
    def __init__(self, label, load, modelpath, arraykey, birectional=False):
        self.label = label
        self.load = load
        self.modelpath = modelpath
        self.arraykey = arraykey
        self.birectional = birectional

    # Directed relations
    READ_FOR='READ_FOR', cypher.LOAD_READ_FOR, includes.MODEL_JSON_RELATIONS + "/read_for.json", 'reads_for_subject', True
    READ_AT='READ_AT',  cypher.LOAD_READ_AT, includes.MODEL_JSON_RELATIONS + "/read_at.json", 'reads_at_channel', True
    LOC_AT='LOC_AT',  cypher.LOAD_LOCATED_AT, includes.MODEL_JSON_RELATIONS + "/located_at.json", 'channels_at_location', True
    ABSOLUTE_POWER='POWER',  cypher.LOAD_ABSOLUTE_POWER, includes.MODEL_JSON_RELATIONS + "/absolute_power.json", 'reads_absolute_power', True

    # birectional relation: NEIGHBOUR
    NEIGHBOUR='NEIGHBOUR',  cypher.LOAD_CHANNEL_NEIGHBORS, includes.MODEL_JSON_RELATIONS + "/assesses.json", 'assesses', False
