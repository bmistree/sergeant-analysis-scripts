import os

from util.file_readers import read_throughput_file, read_latency_file
from util.file_readers import read_fairness_file, read_rtt_latency_file
from util.file_readers import read_speculation_rtt_file
import util.plotters as plotters
import numpy
from modules import register_processor

@register_processor
class LatencyRTTProcessor(object):
    NAME = 'single_node.latency_rtt'

    @staticmethod
    def run(**kwargs):
        '''
        Expected form of kwargs:
            {
                'output_filename': {string} the name of the file to save
                the result to,

                'input_filename': {string} @see
                util.file_readers.read_latency_file for exepcted format of
                file named by input_filename
            }
        '''
        output_filename = kwargs.get('output_filename',None)
        input_filename = kwargs.get('input_filename',None)

        if (output_filename is None) or (input_filename is None):
            assert False

        # each element of this list is a 
        latency_list = read_rtt_latency_file(input_filename)

        with open(output_filename,'w') as fd:
            fd.write('Controller-switch RTT')
            fd.write('\t')
            fd.write('Median latency\n')
            for latency_result in latency_list:
                fd.write(str(latency_result.artificial_rtt_ms))
                fd.write('\t')
                fd.write(str(latency_result.median_latency_ms()))
                fd.write('\n')

@register_processor
class Throughput(object):
    NAME = 'single_node.throughput'

    @staticmethod
    def run(**kwargs):
        '''
        Expected form of kwargs:
            {
                'output_filename': {string} the name of the file to save
                the result to,

                'input_filename': {string} @see
                util.file_readers.read_throughput_file for expected
                format of file named by input_filename.

                'xlabel': {string} The label to use on the x axis of
                the throughput graph.
            }
        '''
        output_filename = kwargs.get('output_filename',None)
        input_filename = kwargs.get('input_filename',None)
        xlabel = kwargs.get('xlabel',None)

        if ((output_filename is None) or (input_filename is None) or
            (xlabel is None)):
            assert False
        
        throughput_list = read_throughput_file(input_filename)
        ylabel = 'Transactions/s\n(thousands)'
        plotters.box_and_whisker_throughput(
            throughput_list,xlabel,ylabel,output_filename)

@register_processor
class LatencyContention(object):
    NAME = 'single_node.latency_contention'

    @staticmethod
    def run(**kwargs):
        '''
        Expected form of kwargs:
            {
                'output_filename': {string} the name of the file to save
                the result to,

                'input_filename': {string} @see
                util.file_readers.read_latency_file for expected
                format of file named by input_filename.
            }
        '''
        output_filename = kwargs.get('output_filename',None)
        input_filename = kwargs.get('input_filename',None)

        if (output_filename is None) or (input_filename is None):
            assert False
            
        latency_list = read_latency_file(input_filename)
        ylabel = 'Program\nLatency(ms)'
        xlabel = 'Contending applications'

        plotters.box_and_whisker_latency(
            latency_list,xlabel,ylabel,output_filename)
            
@register_processor
class ReadOnly(object):
    NAME = 'single_node.read_only'

    @staticmethod
    def run(**kwargs):
        '''
        Expected form of kwargs:
            {
                'output_filename': {string} the name of the file to save
                the result to,

                'input_filename': {string} @see
                util.file_readers.read_latency_file for expected
                format of file named by input_filename.
            }
        '''
        output_filename = kwargs.get('output_filename',None)
        input_filename = kwargs.get('input_filename',None)

        if (output_filename is None) or (input_filename is None):
            assert False

        latency_list = read_latency_file(input_filename)
        # read only latency should only use one thread/switch
        if len(latency_list) != 1:
            print '\nError: read only latency has more entries than expected.\n'
            assert(False)
        latency_result = latency_list[0]

        fifth_percentile = numpy.percentile(latency_result.latency_list_ms,5)
        ninety_fifth_percentile = numpy.percentile(
            latency_result.latency_list_ms,95)
        median = numpy.percentile(latency_result.latency_list_ms,50)
        average = numpy.average(latency_result.latency_list_ms)
        stddev = numpy.std(latency_result.latency_list_ms)

        with open(output_filename,'w') as fd:
            fd.write('Read only latencies (ms)\n')
            fd.write('5th percentile:\t%f\n' % fifth_percentile)
            fd.write('50th percentile:\t%f\n' % median)
            fd.write('95th percentile:\t%f\n' % ninety_fifth_percentile)
            fd.write('Average:\t%f\n' % average)
            fd.write('Stddev:\t%f\n' % stddev)
            fd.write('Corresponding average throughput (ops/s) for single thread\n')
            # multiplying by 1000 because original numbers are in ms.
            fd.write('Average:\t%f\n' % (1000./average))

@register_processor
class Fairness(object):
    NAME = 'single_node.fairness'

    @staticmethod
    def run(**kwargs):
        '''
        Expected form of kwargs:
            {
                'output_filename': {string} the name of the file to save
                the result to,

                'ralph_algo': {boolean} True if using ralph
                scheduling, False if using wound-wait.
                
                'input_filename': {string} @see
                util.file_readers.read_fairness_file for expected
                format of file named by input_filename.
            }
        '''
        output_filename = kwargs.get('output_filename',None)
        input_filename = kwargs.get('input_filename',None)
        ralph_algo = kwargs.get('ralph_algo',None)

        if ((output_filename is None) or (input_filename is None) or
            (ralph_algo is None)):
            assert False

        # fairness_list contains 0s and 1s.  0s for one principal 1s for
        # the other.  Order of 0s and 1s is the order in which principals
        # were allowed to run their applications.
        fairness_list = read_fairness_file(input_filename,ralph_algo)

        xlabel = 'Transactions'
        ylabel = 'Share'

        plotters.fairness(fairness_list,xlabel,ylabel,output_filename)
