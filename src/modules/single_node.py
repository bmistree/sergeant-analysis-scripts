import sys
import os

from util.file_readers import read_latencies, read_throughputs
import util.other as other

from modules import register_processor

'''
Modules for producing single node data
'''

@register_processor
class FairnessProcessor(object):
    NAME = 'single.fairness'
    
    @staticmethod
    def run(**kwargs):
        '''
        For single node fairness data

        @param {String} output_filename --- Will save data to this file.
        Format of saved data is:

        @param {list} input_tuple_list --- Each element is a dict.
        One key is string, 'wound_wait_on' and points to bool.  Other
        is 'filename' and points to string.
        
        #,#|#,#|#,#|#,#|#
        #,#|#,#|#,#|#,#|#

        where the first number of a line is 1 if running with ralph algo
        and 0 if running with wound-wait; and all other entries have
        format: <which principal ran>|<ns timestamp when ran>
        '''
        output_filename = kwargs.get('output_filename',None)
        input_tuple_list = kwargs.get('input_tuple_list',None)

        if ((input_tuple_list is None) or (output_filename is None)):
            assert False

        output_string = ''
        for wound_wait_filename in input_tuple_list:
            wound_wait_on = wound_wait_filename['wound_wait_on']
            wound_wait_on_string = 'true' if wound_wait_on else 'false'
            fairness_filename = wound_wait_filename['filename']
            
            if wound_wait_on:
                output_string += '0'
            else:
                output_string += '1'
            output_string += ','
            with open(fairness_filename,'r') as fd:
                output_string += fd.read()
            output_string += '\n'

        with open(output_filename,'w') as fd:
            fd.write(output_string)


@register_processor
class ThroughputProcessor(object):
    NAME = 'single.throughput'

    @staticmethod
    def run(**kwargs):
        '''
        For single node throughput data.

        @param {list} input_tuple_list --- Each element is a dict.
        One key is string, 'num_switches' and points to int.  Other is
        'filename' and points to string.  

        @param {String} output_filename --- Will save data to this file.
        Format of saved data is:

        #,#,#,#,#
        #,#,#,#,#
        #,#,#,#,#

        where the first number of a line is the number of switches in the
        experiment and the subsequent numbers in the line represent the
        number of operations per second.
        '''
        output_filename = kwargs.get('output_filename',None)
        input_tuple_list = kwargs.get('input_tuple_list',None)

        if ((input_tuple_list is None) or (output_filename is None)):
            assert False

        output_string = ''
        for filename_num_switches_tuple in input_tuple_list:
            num_switches = filename_num_switches_tuple['num_switches']
            throughput_input_filename = filename_num_switches_tuple['filename']

            throughput_list = read_throughputs(throughput_input_filename)
            output_string += str(num_switches) + ','
            # add string list to output string
            output_string += other.num_list_to_string(throughput_list) + '\n'

        with open(output_filename,'w') as fd:
            fd.write(output_string)

@register_processor
class ReadOnlyProcessor(object):
    NAME = 'single.read_only'

    @staticmethod
    def run(**kwargs):
        '''
        For single node latency data with a single switch.

        @param {String} latency_filename --- Name of file with data.
        
        @param {String} output_filename --- Will save data to this file.
        Format of saved data is:

        #,#,#,#,#

        where the first number of a line is the number of switches in the
        experiment and the subsequent numbers in the line represent the
        time, in ns, that an op took.
        '''
        latency_filename = kwargs.get('latency_filename',None)
        output_filename = kwargs.get('output_filename',None)
        
        latency_list = read_latencies(latency_filename)
        with open(output_filename,'w') as fd:
            fd.write('1,') # running on one switch
            fd.write(other.num_list_to_string(latency_list) + '\n')

@register_processor
class LatencyContentionProcessor(object):
    NAME = 'single.latency_contention'

    @staticmethod
    def run(**kwargs):
        '''
        For single node latency data with an artificial rtt of 2 ms and
        contention on switches.

        @param {String} output_filename --- Will save data to this file.
        Format of saved data is:

        @param {list} input_tuple_list --- Each element is a dict.
        One key is string, 'num_switches' and points to int.  Other is
        'filename' and points to string.

        
        #,#,#,#,#
        #,#,#,#,#
        #,#,#,#,#

        where the first number of a line is the number of switches in the
        experiment and the subsequent numbers in the line represent the
        time, in ns, that an op took.
        '''
        output_filename = kwargs.get('output_filename',None)
        input_tuple_list = kwargs.get('input_tuple_list',None)

        if ((input_tuple_list is None) or (output_filename is None)):
            assert False
            
        output_string = ''
        for filename_num_switches_tuple in input_tuple_list:
            num_switches = filename_num_switches_tuple['num_switches']
            latency_input_filename = filename_num_switches_tuple['filename']
            latency_list = read_latencies(latency_input_filename)

            output_string += str(num_switches) + ','
            # add string list to output string
            output_string += other.num_list_to_string(latency_list) + '\n'

        with open(output_filename,'w') as fd:
            fd.write(output_string)

@register_processor
class LatencyRTTProcessor(object):
    NAME = 'single.latency_rtt'
    
    @staticmethod
    def run(**kwargs):
        '''
        For single node latency data with artificial rtts
        
        @param {list} input_tuple_list --- Each element is a dict.
        One key is string, 'delay_us' and points to int.  Other is
        'filename' and points to string.
        
        @param {String} output_filename --- Will save data to this file.
        Format of saved data is:

        #,#,#,#,#
        #,#,#,#,#
        #,#,#,#,#

        where the first number of a line is the amount of artifical
        latency added between the switches and the controller, in ns, and
        subsequent numbers in the line represent the time, in ns, that an
        op took.
        '''
        output_filename = kwargs.get('output_filename',None)
        input_tuple_list = kwargs.get('input_tuple_list',None)

        if ((input_tuple_list is None) or (output_filename is None)):
            assert False

        output_string = ''
        for filename_delay_us_tuple in input_tuple_list:
            delay_us = filename_delay_us_tuple['delay_us']
            latency_input_filename = filename_delay_us_tuple['filename']

            latency_list = read_latencies(latency_input_filename)
            output_string += str(other.us_to_ns(delay_us)) + ','
            # add string list to output string
            output_string += other.num_list_to_string(latency_list) + '\n'

        with open(output_filename,'w') as fd:
            fd.write(output_string)

