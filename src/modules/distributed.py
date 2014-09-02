import sys
import os

from util.file_readers import read_latencies, read_throughputs
from util.file_readers import read_throughputs_produce_latencies
import util.other as other

'''
Modules for producing distributed data
'''

@register_processor('dist.latency')
def latency(**kwargs):
    #(fq_latency_filename, output_filename):
    '''
    @param {String} fq_input_filenames_list --- Each element is a
    string, which is the fully-qualified name of the input file.
    
    @param {String} output_filename --- Will save data to this file.
    Format of saved data is:

    #,#,#,#,#

    where the first number of a line is the number of switches in the
    experiment and the subsequent numbers in the line represent the
    time, in ns, that an op took.
    '''
    latency_filename = kwargs.get('latency_filename',None)
    output_filename = kwargs.get('output_filename',None)

    if (latency_filename is None) or (output_filename is None):
        assert False
    
    output_string = '1,'
    latency_list = read_latencies(latency_filename)
    output_string += other.num_list_to_string(latency_list) + '\n'

    with open(output_filename,'w') as fd:
        fd.write(output_string)
        
@register_processor('dist.throughput')
def throughput(**kwargs):
    # input_filenames_num_switches_tuple_list, output_filename
    '''
    @param {list} input_filenames_num_switches_tuple_list --- Each
    element is a dict.  One key is string, 'num_switches' and points
    to int.  Other is 'filename' and points to string.
    
    For hardware throughput data with no contention
    
    @param {String} output_filename --- Will save data to this file.
    Format of saved data is:

    #,#,#,#,#
    #,#,#,#,#
    #,#,#,#,#

    where the first number of a line is the number of switches in the
    experiment and the subsequent numbers in the line represent the
    number of operations in seconds.
    '''
    output_filename = kwargs.get('output_filename',None)
    input_filenames_num_switches_tuple_list = kwargs.get(
        'input_filenames_list',None)

    if ((input_filenames_num_switches_tuple_list is None) or
        (output_filename is None)):
        assert False
        
    output_string = ''
    for filename_num_switches_tuple in input_filenames_num_swithes_tuple_list:
        num_switches = filename_num_switches_tuple['num_switches']
        throughput_input_filename = filename_num_switches_tuple['filename']
            
        throughput_list = read_throughputs(throughput_input_filename)
        output_string += str(num_switches) + ','
        # add string list to output string
        output_string += other.num_list_to_string(throughput_list) + '\n'

    with open(output_filename,'w') as fd:
        fd.write(output_string)


# From python3 statistics module
def median(data):
    """Return the median (middle value) of numeric data.

    When the number of data points is odd, return the middle data point.
    When the number of data points is even, the median is interpolated by
    taking the average of the two middle values:

    >>> median([1, 3, 5])
    3
    >>> median([1, 3, 5, 7])
    4.0

    """
    data = sorted(data)
    n = len(data)
    if n == 0:
        raise StatisticsError("no median for empty data")
    if n%2 == 1:
        return data[n//2]
    else:
        i = n//2
        return (data[i - 1] + data[i])/2
    
def _fairness(tag,output_filename):
    '''
    For distributed fairness data
    
    @param {String} output_filename --- Will save data to this file.
    Format of saved data is:

    #,#|#,#|#,#|#,#|#
    #,#|#,#|#,#|#,#|#
    
    where the first number of a line is 1 if running with ralph algo
    and 0 if running with wound-wait; and all other entries have
    format: <which principal ran>|<ns timestamp when ran>
    '''
    output_string = ''
    for wound_wait_on in (True,False):
        wound_wait_on_string = 'wound_wait' if wound_wait_on else 'ralph'
        
        fairness_filename = os.path.join(
            FAIRNESS_FOLDER,
            'dist_fairness_10k_%s_%s.csv' % (tag,wound_wait_on_string))

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
    
        
