import numpy

class LatencyResult(object):
    def __init__(self,num_switches,latency_list_ns,artificial_rtt_ns=0):
        '''
        @param {int} num_switches --- The number of switches used in
        the experiment.

        @param {list} latency_list_ns --- A list of ints.  Each int is
        the number of ns an op took.

        @param {int} artificial_rtt_ns --- the artificial latnecy that
        injected into the system
        '''
        self.num_switches = num_switches
        self.latency_list_ns = latency_list_ns

        self.latency_list_ms = map(
            lambda ns : ns / 1000000.,
            latency_list_ns)

        self.artificial_rtt_ns = artificial_rtt_ns
        self.artificial_rtt_ms = (
            float(artificial_rtt_ns) / 1000000.)
        
    def median_latency_ms(self):
        '''
        @returns {float} --- The median latency of all programs, in
        ms.
        '''
        return numpy.median(self.latency_list_ms)

    def percentile_latency_ms(self,which_percentile):
        return numpy.percentile(self.latency_list_ms,which_percentile)
