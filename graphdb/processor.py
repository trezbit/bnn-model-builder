'''Batch processor for the graph model'''
import json
from config import includes
import os

from graphdb.bntypes import EEGReadMode, NodeType, RelationType
from utils import ioutil
from graphdb.connector import NEO4JConnector
from graphdb.cypher import *
from graphdb.studymodel import SubjectNode, ReadNode, WaveType



class GraphProcessor():
    '''Batch node/relation processor for the graph model'''
    # Constructor
    def __init__(self, config={}):
        self.config = config
        self.connector = NEO4JConnector()

    # Destructor
    def __del__(self):
        self.connector.close()

    def cleanup_graph(self):
        '''Main method for cleaning up the graph'''
        print("Cleanup Graph")
        self.connector.cleanup_full()
        return
    
    def cleanup_study_graph(self):
        '''Method for cleaning up the study sub graph'''
        print("Cleanup Graph")
        self.connector.cleanup_study()
        return
    
    def build_topology_graph(self):
        '''Main method for building the graph'''
        print("Build Graph")
        self.cleanup_graph()
        self.build_node(NodeType.BRAINREG)
        self.build_node(NodeType.CHANNEL)
        self.build_relation(RelationType.LOC_AT)
        self.build_relation(RelationType.CHAIN_NEXT)
        self.build_node(NodeType.WAVE)
        return
    
    def build_node(self, nodetype:NodeType):
        '''Main method for building nodes for batch upload'''
        print("Build Nodes - Label:", nodetype.load)
        newconst = CREATE_CONSTRAINT.replace("__LABEL__", nodetype.label)
        self.connector.run_query(newconst)
        newfulltext = CREATE_FULLTEXT_INDEX.replace("__LABEL__", nodetype.label)
        self.connector.run_query(newfulltext)
        self.connector.run_query(nodetype.load)
        
        
        return
    
    def build_relation(self, reltype:RelationType):
        '''Main method for building relations for batch upload'''
        print("Build Relations -  Type: ", reltype.load)
        self.connector.run_query(reltype.load)

        return

    
    def build_eegstudy_subgraph(self, params={}):
        '''Main method for building the EEG READ graph with study subjects, channels, and Absolute Powers nodes and relations'''
        print("Build EEG Study Subgraph")
        self.cleanup_study_graph()
        self.build_node(NodeType.SUBJECT)
        self.build_node(NodeType.READS)
        self.build_relation(RelationType.READ_FOR)
        self.build_relation(RelationType.READ_AT)
        self.build_relation(RelationType.ABS_POWER)
        return
    

    def extract_study_model(self, params={}):
        '''Main method for extracting subjects, channel reads and absolute powers  from the EEG STUDY data'''
        print("Extract Subjects")
        subjects = dict()
        readings = dict()

        subjbaseid = 1000
        readsbaseid = 10000

        channelsdict = ioutil.load_json_to_dict(NodeType.CHANNEL.arraykey, "Name", NodeType.CHANNEL.modelpath)
        #print("Channels:", channelsdict)

        for study in includes.STUDY_DATA:
            print("Study:", study)
            studydir = includes.STUDY_DATA[study]["loc"]            
            painmarker = includes.STUDY_DATA[study]["pain"]

            for root, dirs, files in os.walk(studydir):
                for subjdir in dirs:
                    #subjdir = os.path.basename(os.path.normpath(root))
                    # print("Subject:", subjdir)
                    subjbaseid += 1
                    subject = SubjectNode(subjbaseid, subjdir, painmarker)
                    # print("Subject Node:", subject)
                    subjects[subjdir] = subject.getSerializableDict()

                    # Eyes Closed Read
                    studychannel= ioutil.read_json_to_dict(os.path.join(root, subjdir, EEGReadMode.EC.name + "_channels.json"))
                    #print("Study Channels:", studychannel[0])
                    ecread=os.path.join(root, subjdir, EEGReadMode.EC.name + "_powers.csv")
                    reads= ioutil.read_csv_to_dict(ecread)
                    for read in reads:
                        # print("EC Read:", read)
                        # check if read is of type dictionary
                        if read is not None and isinstance(read, dict):
                            readsbaseid += 1
                            chanlabelindex = int(read['channel'])-1
                            readchannel = studychannel[chanlabelindex]["labels"]
                            #print("Read Channel:", readchannel)
                            #print("Read:", chanlabelindex)
                            # skip if the channel is not in the channels dictionary
                            if readchannel not in channelsdict:
                                continue
                            readatref = channelsdict[readchannel]["ID"]
                            readname = subjdir + "_" + readchannel + "." + EEGReadMode.EC.name
                            readnode = ReadNode(readsbaseid, readname, EEGReadMode.EC.name, subjbaseid, readatref)
                            readnode.setWaveAbsPower(read['alphaPower'],read['betaPower'],read['deltaPower'],read['thetaPower'],read['gammaPower'])
                            #print("EC Read Node:", readnode.getDict())
                            print("EC Read Node:", readnode.getSerializableDict())
                            print("EC Read Name:", readname)
                            readings[readname] = readnode.getSerializableDict()

                    # Eyes Open Read
                    # Ensure that the read data exists
                    if not os.path.exists(os.path.join(root, subjdir, EEGReadMode.EO.name + "_powers.csv")):
                        continue
                    studychannel= ioutil.read_json_to_dict(os.path.join(root, subjdir, EEGReadMode.EO.name + "_channels.json"))
                    eoread=os.path.join(root, subjdir, EEGReadMode.EO.name + "_powers.csv")
                    reads= ioutil.read_csv_to_dict(eoread)
                    for read in reads:
                        # check if read is of type dictionary
                        if read is not None and isinstance(read, dict):
                            readsbaseid += 1
                            chanlabelindex = int(read['channel'])-1
                            readchannel = studychannel[chanlabelindex]["labels"]
                            # skip if the channel is not in the channels dictionary -- handling some weird .m outputs
                            if readchannel not in channelsdict:
                                continue
                            readatref = channelsdict[readchannel]["ID"]
                            readname = subjdir + "_" + readchannel + "." + EEGReadMode.EO.name
                            readnode = ReadNode(readsbaseid, readname, EEGReadMode.EO.name, subjbaseid, readatref)
                            readnode.setWaveAbsPower(read['alphaPower'],read['betaPower'],read['deltaPower'],read['thetaPower'],read['gammaPower'])
                            readings[readname] = readnode.getSerializableDict()

        ioutil.write_dict_to_json(subjects, NodeType.SUBJECT.modelpath)
        ioutil.write_dict_to_json(readings, NodeType.READS.modelpath)

        return
    

    def export_study_subgraph(self, params={"EC_Only":True}):
        '''Main method for exporting the EEG READ graph with study subjects, channels, and Absolute Powers nodes and relations'''
        print("Export EEG Study Subgraph")

        # Export Nodes
        # Export Subjects
        subjectdict = ioutil.read_json_to_dict(NodeType.SUBJECT.modelpath)
        nodeattrs = SubjectNode.getGraphNodeAttributes()
        subjects=[]
        for subj in subjectdict:
            subject = []
            for attr in nodeattrs["attrref"]:
                subject.append(subjectdict[subj][attr])
            subjects.append(subject)
        ioutil.write_array_to_csv(subjects, nodeattrs["header"], includes.MODEL_CSV_BASE + "/node." + NodeType.SUBJECT.label.lower() + ".csv")
        # Export Reads
        readdict = ioutil.read_json_to_dict(NodeType.READS.modelpath)
        nodeattrs = ReadNode.getGraphNodeAttributes()
        reads=[]
        for readi in readdict:
            read = []
            for attr in nodeattrs["attrref"]:
                read.append(readdict[readi][attr])
            reads.append(read)
        ioutil.write_array_to_csv(reads, nodeattrs["header"], includes.MODEL_CSV_BASE + "/node." + NodeType.READS.label.lower() + ".csv")

        
        # Export Edges
        # Export Read For & Read At
        readforedges = []
        readatedges = []
        readfor_attrs = ReadNode.getGraphEdgeAttributes(RelationType.READ_FOR.name)
        readat_attrs = ReadNode.getGraphEdgeAttributes(RelationType.READ_AT.name)
        # Export Abs Power
        abspoweredges = []
        abspower_attrs = ReadNode.getGraphEdgeAttributes(RelationType.ABS_POWER.name)
        powers = [WaveType.ALPHA.name, WaveType.BETA.name, WaveType.DELTA.name, WaveType.THETA.name, WaveType.GAMMA.name]

        for readi in readdict:
            rfedge = []
            ratedge = []
            for attr in readfor_attrs["attrref"]:
                rfedge.append(readdict[readi][attr])
            readforedges.append(rfedge)
            for attr in readat_attrs["attrref"]:
                ratedge.append(readdict[readi][attr])
            readatedges.append(ratedge)
            for power in powers:
                abspedge = []
                
                abspedge.append(readdict[readi][abspower_attrs["attrref"][0]])
                if power == WaveType.ALPHA.name:
                    abspedge.append(WaveType.ALPHA.idref)
                elif power == WaveType.BETA.name:
                    abspedge.append(WaveType.BETA.idref)
                elif power == WaveType.DELTA.name:
                    abspedge.append(WaveType.DELTA.idref)
                elif power == WaveType.THETA.name:
                    abspedge.append(WaveType.THETA.idref)
                elif power == WaveType.GAMMA.name:
                    abspedge.append(WaveType.GAMMA.idref)
                else :
                    continue
                abspedge.append(readdict[readi][power])
                abspoweredges.append(abspedge)
            
        ioutil.write_array_to_csv(readforedges, readfor_attrs["header"], includes.MODEL_CSV_BASE + "/edge." + RelationType.READ_FOR.label.lower() + ".csv")
        ioutil.write_array_to_csv(readatedges, readat_attrs["header"], includes.MODEL_CSV_BASE + "/edge." + RelationType.READ_AT.label.lower() + ".csv")
        ioutil.write_array_to_csv(abspoweredges, abspower_attrs["header"], includes.MODEL_CSV_BASE + "/edge." + RelationType.ABS_POWER.label.lower() + ".csv")
        
        return


         
        