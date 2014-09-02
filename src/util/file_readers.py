import other

# Java's jit compiler makes code go faster and faster as it runs.  To
# avoid the effects of this, filter out this fraction of traces from
# data and use rest.
DEFAULT_WARMUP_FRACTION = .5

# For throughput, divide traces into .5 second bins.  Calculate the
# throughput across that bin.
SAMPLE_LENGTH_SECONDS = .5

def read_throughputs_produce_latencies(
    filename,warmup_fraction=DEFAULT_WARMUP_FRACTION):
    '''
    @param {string} filename ---

    #,#,#,#
    #,#,#,#
    ...

    Each number is the time (in ns) at which an operation committed.
    Take deltas between successive numbers to generate latencies.
    
    @returns {list} --- A list of ints, each representing the number
    of nanoseconds an operation took.
    '''
    # single_file_data is a list containing separate lists.  Each list
    # contains timestamps from a single application's operations.
    single_file_data = _read_single_file_data(filename)

    # first take deltas to produce latencies
    latency_data = []
    for single_application_data in single_file_data:
        single_latency_app_data = []
        latency_data.append(single_latency_app_data)
        for i in range(1,len(single_application_data)):
            prev = single_application_data[i-1]
            current = single_application_data[i]

            latency = current-prev
            # sanity check
            if latency < 0:
                print '\nShould never get negative latencies\n'
                assert False
            
            single_latency_app_data.append(latency)

    # now filter out warmup
    warmed_up_latency_data = []
    for single_latency_data in latency_data:
        single_warmed_up_latency = (
            single_latency_data[int(len(single_latency_data)*warmup_fraction):],
            single_latency_data)
        warmed_up_latency_data.append(single_warmed_up_latency)

    # now collapse all lists into one
    to_return = []
    for single_warmed_up_latency in warmed_up_latency_data:
        to_return += single_warmed_up_latency
    return to_return


def read_throughputs(filename,warmup_fraction=DEFAULT_WARMUP_FRACTION):
    '''
    @returns {list} --- A list of floats, each representing number of
    ops/s
    '''
    # single_file_data is a list containing separate lists.  Each
    # list contains timestamps from a single switch's operations.
    single_file_data = _read_single_file_data(filename)
    return _find_throughput(single_file_data)

def _find_throughput(times,sample_length_seconds=SAMPLE_LENGTH_SECONDS,
                     warmup_fraction=DEFAULT_WARMUP_FRACTION):
    '''
    @param {list of lists} times --- A list of lists.  Each internal
    list contains a timestamp for when an operation completed.

    @returns {list} --- A list of floats, each representing number of
    ops/s
    '''
    start, end = _find_window(times, warmup_fraction)

    # trimmed is all entries in times that was between start and end.
    trimmed = [ [ t for t in arr if t >= start and t <= end ] for arr in times ]

    num_switches = len(trimmed)
    all_trimmed_data = []
    for switch_data_list in trimmed:
        all_trimmed_data += switch_data_list

    # should contain ns timestamps of all generated data
    sorted_data = sorted(all_trimmed_data)

    # normalize so that beginning of data start at 0
    earliest_data = sorted_data[0]
    sorted_data = map(
        lambda d : d - earliest_data,
        sorted_data)
    data_in_s = map(
        lambda d : other.ns_to_s(d),
        sorted_data)

    bucket_count_dict = {}
    for datum in data_in_s:
        time_bucket = int (datum / sample_length_seconds)
        current_count = bucket_count_dict.setdefault(time_bucket,0)
        bucket_count_dict[time_bucket] = current_count + 1
    
    # get rid of last element, in case it didn't run an integer
    # divisible amount of time.
    del bucket_count_dict[time_bucket]
    counts_per_period = bucket_count_dict.values()
    throughput_ops_per_second = map(
        lambda count : count / sample_length_seconds,
        counts_per_period)
    
    return throughput_ops_per_second

def _find_window(times, warmup_fraction):
    """Finds the window of data we want to use.
    We only want times when all threads were running.
    Returns (start, end)
    Cuts out the first warmup proportion of the time"""
    last_start = max([ t[0] for t in times])
    first_end = min([ t[-1] for t in times])

    # do warmup
    end = first_end
    warmup_time = (end - last_start) * warmup_fraction
    start = last_start + warmup_time
    return (start, end)
        


def read_latencies(filename,warmup_fraction=DEFAULT_WARMUP_FRACTION):
    '''
    @param {String} filename --- The fully-qualified name of a file to
    read data from.  The file should be formatted as follows:

    #,#,#,#
    #,#,#,#
    ...

    Ie., each line contains comma-separated numbers.  The numbers are
    in nanoseconds.

    @param {float} warmup_fraction --- 0 to 1.  What fraction of
    values we should truncate to account for warmup.

    @returns {list} --- Each element is an integer, providing the
    nanosecond timestamp of the number.
    '''
    
    list_of_list_of_timestamps = _read_single_file_data(filename)
    ### perform warmup truncation
    list_of_list_of_timestamps = map(
        lambda internal_list:
            internal_list[ int(len(internal_list)*warmup_fraction):],
        list_of_list_of_timestamps)
    
    ### reduce list of lists to a single list
    latencies_list = reduce(
        lambda cumulative_list, element_list : cumulative_list + element_list,
        list_of_list_of_timestamps,[])

    return latencies_list


def _read_single_file_data(filename):
    '''
    @returns {list} --- Each list contains a list of numbers.  The
    numbers are nanosecond timestamps for each operation that a switch
    performs.
    '''
    to_return = []
    fd = open(filename,'r')
    for switch_line in fd:
        to_return.append(_read_switch_line(switch_line))
    fd.close()
    return to_return

def _read_switch_line(single_switch_data_string):
    '''
    @param {string} single_switch_data_string ---- comma-separated
    string containing numbers.
    
    @returns {list} --- Each element is an integer.
    '''
    entries = single_switch_data_string.split(',')
    # remove whitespace
    entries = filter(
        lambda entry: entry.strip() != '',
        entries)
    return map(
        lambda x: int(x),
        entries)
