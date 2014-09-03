#!/usr/bin/env python
import argparse
import sys

from util.cfg_reader import read_config
import modules.modules
from modules.modules import get_processor

import modules.distributed

def run():
    config_list = parse_cfg()
    for processor_job in config_list:
        processor = get_processor(processor_job['name'])
        processor.run(**processor_job['args'])
    

def parse_cfg():
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

    config_list = read_config(cfg_filename)
    return config_list
    
    
if __name__ == '__main__':
    run()
