'''Main entry point for the application'''
import argparse

import graphdb.connector as conn
import graphdb.processor as processor



def test_neo4j(params):
    '''Test Neo4j connectivity'''
    print("Test Neo4j connectivity - Config:", params)
    neocl = conn.NEO4JConnector()
    if params == '{}':
        neocl.verify_connectivity()
    elif params == 'clean':
        neocl.cleanup_full()
    neocl.close()


def parse_args():
    '''CLI Argument parser for the application'''
    parser = argparse.ArgumentParser(description='BrainNet (BN) graph db build utilities and queries')
    subparser = parser.add_subparsers(dest='command')

    tester = subparser.add_parser('test', help='(BN) tester utilities for Neo4j')
    builder = subparser.add_parser('build', help='EEG read, channels and topology build utilities')


    convertgroup1 = tester.add_mutually_exclusive_group(required=True)
    convertgroup1.add_argument('--neo4j'
                               , help='Test Neo4j connectivity'
                               , nargs='?', const='{}', type=str)
    
    convertgroup2 = builder.add_mutually_exclusive_group(required=True)
    convertgroup2.add_argument('--topo'
                               , help='Build Ref Topology Graph'
                               , nargs='?', const='{}', type=str)
    convertgroup2.add_argument('--study'
                               , help='Build EEG Reads Study Graph'
                               , nargs='?', const='{}', type=str)
    convertgroup2.add_argument('--eegreads'
                               , help='Build EEG Reads Graph'
                               , nargs='?', const='{}', type=str)
    
    convertgroup2.add_argument('--export'
                               , help='Export EEG Study Subgraph to CSV'
                               , nargs='?', const='{}', type=str)

    builder.add_argument('--debug', help='Log/Data structures output', type=str, required=False)

    args = parser.parse_args()
    return args

def run_session (args):
    '''Run session for the application'''
    #pprint.pprint(args)
    if args.command is None:
        print("Undefined utility command. Options: test, build")
    elif (args.command == 'test' and args.neo4j is not None):
        test_neo4j(args.neo4j)
    elif (args.command == 'build' and args.topo is not None):
        processor.GraphProcessor().build_topology_graph()
    elif (args.command == 'build' and args.study is not None):
        processor.GraphProcessor().build_eegstudy_subgraph()
    elif (args.command == 'build' and args.eegreads is not None):
        processor.GraphProcessor().extract_study_model()
    elif (args.command == 'build' and args.export is not None):
        processor.GraphProcessor().export_study_subgraph()
    else:
        print("Unknown utility test command option for: "    , args.command)
    print("\nEnd of demo session...", args.command)

if __name__ == '__main__':
    builder_args = parse_args()
    run_session(builder_args)
