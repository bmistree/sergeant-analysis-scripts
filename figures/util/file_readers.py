from throughput_results import ThroughputResult
from latency_result import LatencyResult

def read_speculation_rtt_file(input_filename):
    '''
    For anyware speculation latency data with artificial rtts
    
    @param {String} input_filename --- Name of file to import data
    from.  Expected format of data file is:

    #,#,#,#,#
    #,#,#,#,#
    #,#,#,#,#

    where the first number of a line is a 0 if speculation is off and
    a 1 if speculation is on; the second number of the file is the
    artificially added rtt (in ns); and subsequent numbers in the line
    represent the time, in ns, that an op took.

    @returns {2-tuple} (a,b)
    
       a --- A list of LatencyResult objects with speculation off,
             sorted in ascending order of rtt.
       
       b --- A list of LatencyResult objects with speculation on,
             sorted in ascending order of rtt.
    '''
    speculation_off_list = []
    speculation_on_list = []

    with open(input_filename) as fd:
        for line in fd:
            line = line.strip()
            token_list = line.split(',')

            speculation_token = int(token_list[0])
            rtt_token = int(token_list[1])
            string_latencies = token_list[2:]

            latencies_ns = map(
                lambda string: int(string),
                string_latencies)

            latency_result = LatencyResult(1,latencies_ns,rtt_token)
            # ugh: hard-coding here...
            if speculation_token == 1:
                speculation_on_list.append(latency_result)
            else:
                speculation_off_list.append(latency_result)

    # sort to_return in ascending order of number of switches used
    speculation_off_list.sort(
        key = lambda latency_result: latency_result.artificial_rtt_ms)
    speculation_on_list.sort(
        key = lambda latency_result: latency_result.artificial_rtt_ms)
    
    return (speculation_off_list, speculation_on_list)


def read_fairness_file(input_filename,ralph_algo):
    '''
    @param {String} input_filename --- Name of file to import data
    from.  Expected format of data file is:

    #,#|#,#|#,#|#,#|#
    #,#|#,#|#,#|#,#|#
    
    where the first number of a line is 1 if running with ralph algo
    and 0 if running with wound-wait; and all other entries have
    format: <which principal ran>|<ns timestamp when ran>
    
    @param {boolean} ralph_algo --- True if using ralph scheduling,
    False if using wound-wait.

    @returns {list} --- Each element of list is either 0 or 1
    corresponding to which principal executed.
    '''
    to_return = []
    with open(input_filename) as fd:
        for line in fd:
            line = line.strip()
            # ignores any empty lines
            if line == '':
                continue
            
            token_list = line.split(',')
            which_algo = int(token_list[0])
            if which_algo == ralph_algo:
                # using -1 because token_list has a trailing , at end.
                op_list = token_list[1:-1]
                
                # op_list is a list of strings with the following
                # structure: '<princ num: 0 or 1>|<timestamp>' Just
                # getting out the principal number (as a number)
                to_return = map(
                    lambda op: int(op.split('|')[0]),
                    op_list)
                return to_return

    print '\nIncorrectly formatted fairness file\n'
    assert False
            

def read_latency_file(input_filename):
    '''
    @param {String} input_filename --- Name of file to import data
    from.  Expected format of data file is:

    #,#,#,#,#
    #,#,#,#,#
    #,#,#,#,#

    where the first number of a line is the number of switches in the
    experiment and the subsequent numbers in the line represent the
    time, in ns, that an op took.

    @returns {list} --- Each element of list is a LatencyResult
    object.  List is sorted by number of switches running, in
    ascending order.
    '''
    to_return = []

    with open(input_filename) as fd:
        for line in fd:
            # ignores any empty lines
            if line == '':
                continue

            single_run_data = _comma_separated_string_to_float_list(
                line)
            num_switches = int(single_run_data[0])
            latency_data_ns = single_run_data[1:]

            to_return.append(LatencyResult(num_switches,latency_data_ns))

    # sort to_return in ascending order of number of switches used
    to_return.sort(
        key = lambda latency_result: latency_result.num_switches)
            
    return to_return

def read_rtt_latency_file(input_filename):
    '''
    @param {String} input_filename --- Name of file to import data
    from.  Expected format of data file is:

    #,#,#,#,#
    #,#,#,#,#
    #,#,#,#,#

    where the first number of a line is the artificial rtt delay, in
    ns, between the switch and controller and the subsequent numbers
    in the line represent the time, in ns, that an op took.

    @returns {list} --- Each element of list is a LatencyResult
    object.  List is sorted by artificial latency, in ascending order.
    '''
    to_return = []

    with open(input_filename) as fd:
        for line in fd:
            # ignores any empty lines
            if line == '':
                continue

            single_run_data = _comma_separated_string_to_float_list(
                line)
            artificial_latency_ns = int(single_run_data[0])
            latency_data_ns = single_run_data[1:]

            to_return.append(
                LatencyResult(1,latency_data_ns,artificial_latency_ns))

    # sort to_return in ascending order of rtt latency
    to_return.sort(
        key = lambda latency_result: latency_result.artificial_rtt_ms)
            
    return to_return



def read_throughput_file(input_filename):
    '''
    @param {String} input_filename --- Name of file to import data
    from.  Expected format of data file is:
    
    #,#,#,#,#
    #,#,#,#,#
    #,#,#,#,#

    where the first number of a line is the number of switches in the
    experiment and the subsequent numbers in the line represent the
    number of operations per second.

    @returns {list} --- Each element of list is a ThroughputResult
    object.  List is sorted by number of switches running, in
    ascending order.
    '''
    to_return = []

    with open(input_filename) as fd:

        for line in fd:
            # ignores any empty lines
            if line == '':
                continue

            single_run_data = _comma_separated_string_to_float_list(
                line)
            num_switches = int(single_run_data[0])
            throughput_data = single_run_data[1:]

            to_return.append(ThroughputResult(num_switches,throughput_data))

    # sort to_return in ascending order of number of switches used
    to_return.sort(
        key = lambda throughput_result: throughput_result.num_switches)
            
    return to_return
            
def _comma_separated_string_to_float_list(line):
    '''
    @param {String} line --- comma-separated string of numbers.

    @returns{list} --- Each element is a float.
    '''
    string_list = line.split(',')
    float_list = map(
        lambda string : float(string),
        string_list)
    return float_list

