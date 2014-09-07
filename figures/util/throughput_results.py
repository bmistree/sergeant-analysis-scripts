
class ThroughputResult(object):
    def __init__(self,num_switches,throughput_list):
        '''
        @param {int} num_switches --- The number of switches used in
        the experiment.

        @param {list} throughput_list --- A list of floats.  Each
        float is ops/s.
        '''
        self.num_switches = num_switches
        self.throughput_list = throughput_list

        self.throughput_list_ks_per_second = map(
            lambda throughput_num: throughput_num/1000.,
            throughput_list)
