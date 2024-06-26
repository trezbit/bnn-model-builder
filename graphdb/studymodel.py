'''BrainNet Study Model Definitions'''
import os
import json
from .bntypes import NodeType, RelationType, WaveType

# make all CSF objects JSON friendly
class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class ModelBase(object):
    def __init__(self, id, name, typedef):
        self.id = id
        self.name = name
        self.typedef = typedef
    def setName(self, name):
        self.name = name
    def getName(self):
        return self.name
    def getDict(self):
        return self.__dict__
    def setId(self, id):
        self.id = id
    def getId(self):
        return self.id  
    def getTypeDef(self):
        return self.typedef
    
class SubjectNode(ModelBase):
    # Constructor
    def __init__(self, id, name, pain_marker):
        self.nodetype = NodeType.SUBJECT
        self.pain = pain_marker
        ModelBase.__init__(self,id, name, NodeType.SUBJECT.label)
    
    def hasPainMarker(self):
        return self.functional_category

    def getSerializableDict(self):
        sdict = {}
        sdict["id"] = self.id
        sdict["name"] = self.name
        sdict["pain"] = self.pain
        return sdict
    
    #define static methods
    @staticmethod
    def getGraphNodeAttributes() -> dict:
        return { "header": ["ID", "Name", "PainMarker"], "attrref": ["id", "name", "pain"]}
    

class ReadNode(ModelBase):
    # Constructor
    def __init__(self, id, name,read_type, read_for, read_at):
        # EC: Eyes Closed vs EO: Eyes Open
        self.read_type = read_type
        self.read_for = read_for
        self.read_at = read_at
        self.wave_abs_powers = { WaveType.ALPHA.name: 0.0, WaveType.BETA.name: 0.0, WaveType.DELTA.name: 0.0, WaveType.THETA.name: 0.0, WaveType.GAMMA.name: 0.0}

        ModelBase.__init__(self,id, name, NodeType.READS.label)    
    def getReadType(self):
        return self.display_name
    def setReadType(self, read_type):
        self.display_name = read_type
    def getReadFor(self):
        return self.read_for
    def setReadFor(self, read_for):
        self.read_for = read_for
    def getReadAt(self):
        return self.read_at
    def setReadAt(self, read_at):
        self.read_at = read_at
    
    def getSerializableDict(self):
        sdict = {}
        sdict["id"] = self.id
        sdict["name"] = self.name
        sdict["read_type"] = self.read_type
        sdict["read_for"] = self.read_for
        sdict["read_at"] = self.read_at
        sdict[WaveType.ALPHA.name] = self.wave_abs_powers[WaveType.ALPHA.name]
        sdict[WaveType.BETA.name] = self.wave_abs_powers[WaveType.BETA.name]
        sdict[WaveType.DELTA.name] = self.wave_abs_powers[WaveType.DELTA.name]
        sdict[WaveType.THETA.name] = self.wave_abs_powers[WaveType.THETA.name]
        sdict[WaveType.GAMMA.name] = self.wave_abs_powers[WaveType.GAMMA.name]
        return sdict
    
    def setWaveAbsPower(self, alpha, beta, delta, theta, gamma):
        self.wave_abs_powers[WaveType.ALPHA.name] = alpha
        self.wave_abs_powers[WaveType.BETA.name] = beta
        self.wave_abs_powers[WaveType.DELTA.name] = delta
        self.wave_abs_powers[WaveType.THETA.name] = theta
        self.wave_abs_powers[WaveType.GAMMA.name] = gamma


    #define static methods
    @staticmethod
    def getGraphNodeAttributes() -> dict:
        return { "header": ["ID", "Name", "ReadMode"], "attrref": ["id", "name", "read_type"]}
    @staticmethod
    def getGraphEdgeAttributes(edge) -> dict:
        attrdefs = {}
        if edge == RelationType.READ_FOR.name:
            attrdefs = { "header": ["FromID", "ToID"], "attrref": ["id", "read_for"]}
        elif edge == RelationType.READ_AT.name:
            attrdefs = { "header": ["FromID", "ToID"], "attrref": ["id", "read_at"]}
        else:
            attrdefs = { "header": ["FromID", "ToID", "Weight"], "attrref": ["id","idref"]}
        return attrdefs




    




