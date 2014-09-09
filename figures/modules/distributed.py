import os

from util.file_readers import read_throughput_file, read_latency_file
import util.plotters as plotters
from modules import register_processor


@register_processor
class Throughput(object):
    NAME = 'dist.throughput'

    @staticmethod
    def run(**kwargs):
        '''
        kwargs has form:
        {
            "output_filename": {String} name of file to output,
            "input_filename": {String} name of file to input from
        }
        '''
        output_filename = kwargs.get('output_filename',None)
        input_filename = kwargs.get('input_filename',None)

        if (output_filename is None) or (input_filename is None):
            assert False
        
        throughput_list = read_throughput_file(input_filename)
        ylabel = 'Transactions/s\n(thousands)'
        xlabel = 'Parallel applications'

        plotters.box_and_whisker_throughput(
            throughput_list,xlabel,ylabel,output_filename)

@register_processor
class SpeculativeLatency(object):
    NAME = 'dist.speculative_latency'

    @staticmethod
    def run(**kwargs):
        '''
        kwargs has form:
        {
            "output_filename": {String} name of file to output,
            "input_speculation_on_filename": {String} name of file to input from
            "input_speculation_off_filename": {String} name of file to input from
        }
        '''
        output_filename = kwargs.get('output_filename',None)
        input_speculation_on_filename = kwargs.get(
            'input_speculation_on_filename',None)
        input_speculation_off_filename = kwargs.get(
            'input_speculation_off_filename',None)

        if ((output_filename is None) or
            (input_speculation_on_filename is None) or
            (input_speculation_off_filename is None)):
            assert False

        speculation_latency_list = read_latency_file(input_speculation_on_filename)
        no_speculation_latency_list = read_latency_file(input_speculation_off_filename)

        if ((len(speculation_latency_list) != 1) or
            (len(no_speculation_latency_list) != 1)):
            print (
                '\nError in distributed speculative latency: expect only a ' +
                'single latency entry per topology.\n')
            assert False
        speculation_latency_result = speculation_latency_list[0]
        no_speculation_latency_result = no_speculation_latency_list[0]

        with open(output_filename,'w') as fd:
            fd.write('Speculation 5th latnecy (ms): ')
            fd.write(str(speculation_latency_result.percentile_latency_ms(5)))
            fd.write('\n')
            fd.write('Speculation median latnecy (ms): ')
            fd.write(str(speculation_latency_result.median_latency_ms()))
            fd.write('\n')
            fd.write('Speculation 95th latnecy (ms): ')
            fd.write(str(speculation_latency_result.percentile_latency_ms(95)))
            fd.write('\n')
            fd.write('\n')
            fd.write('No speculation 5th latnecy (ms): ')
            fd.write(str(no_speculation_latency_result.percentile_latency_ms(5)))
            fd.write('\n')
            fd.write('No speculation median latnecy (ms): ')
            fd.write(str(no_speculation_latency_result.median_latency_ms()))
            fd.write('\n')
            fd.write('No speculation 95th latnecy (ms): ')
            fd.write(str(no_speculation_latency_result.percentile_latency_ms(95)))
            fd.write('\n')

@register_processor
class Latency(object):
    NAME = 'dist.latency'

    @staticmethod
    def run(**kwargs):
        '''
        kwargs has form:
        {
            "output_filename": {String} name of file to output,
            "input_tree_filename": {String} name of file to input from
            "input_linear_filename": {String} name of file to input from
        }
        '''

        output_filename = kwargs.get('output_filename',None)
        input_filename_tree = kwargs.get('input_tree_filename',None)
        input_filename_linear = kwargs.get('input_linear_filename',None)

        if ((output_filename is None) or
            (input_filename_tree is None) or
            (input_filename_linear is None)):
            assert False
        
        # each should only have a single entry in it.  Check
        tree_latency_list = read_latency_file(input_filename_tree)
        linear_latency_list = read_latency_file(input_filename_linear)

        if (len(tree_latency_list) != 1) or (len(linear_latency_list) != 1):
            print (
                '\nError in distributed latency: expect only a ' +
                'single latency entry per topology.\n')
            assert False

        tree_latency_result = tree_latency_list[0]
        linear_latency_result = linear_latency_list[0]

        with open(output_filename,'w') as fd:
            fd.write('Tree median latnecy (ms): ')
            fd.write(str(tree_latency_result.median_latency_ms()))
            fd.write('\n')
            fd.write('Linear median latnecy (ms): ')
            fd.write(str(linear_latency_result.median_latency_ms()))
            fd.write('\n')
