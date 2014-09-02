#!/usr/bin/env python
import argparse
import sys

from util.cfg_reader import read_config

# Keys are strings, values are functions for processing data.  When we
# encounter a key in our dictionary from reading the config file, the
# value of the key are the arguments that get passed to the function.
available_processes = {}


import modules.distributed


def run():
    description_string = '''
Use this script to process experimental data.
'''
    parser = argparse.ArgumentParser(description=description_string)
    parser.add_argument(
        '--cfg',
        help='Configuration filename (should be json)')
    args = parser.parse_args()
    

    if args.cfg is None:
        print '\nRequire a configuration filename.\n'
        sys.exit(-1)
    else:
        cfg_filename = args.cfg

    config_dict = read_config(cfg_filename)
    
    
if __name__ == '__main__':
    run()
