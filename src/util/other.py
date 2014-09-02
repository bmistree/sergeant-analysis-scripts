
def ns_to_s(ns):
    return ns / 1000000000.

def us_to_ns(us):
    '''
    @param {int} us --- Time, in microseconds.

    @returns {int} --- Time, in nanoseconds.
    '''
    return us*1000
    

def num_list_to_string(num_list):
    '''
    @param {list} num_list --- Each element is an integer.

    @returns {String} --- A comma-separated list of numbers.
    '''
    # convert num list to string list
    string_list = map(
        lambda num : str(num), num_list)
    return ','.join(string_list)

