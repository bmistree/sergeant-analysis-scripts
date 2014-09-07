import matplotlib.pyplot as plt
import pylab
import numpy
import math

BAR_CHART_COLOR_VEC = ['#c34343', # reddish
                       '#535050', # gray
                       ]
    
def fairness(principal_list,xlabel,ylabel,output_filename):
    '''
    @param {list} principal_list --- Each element is either a 0 or a
    1.  0 if transaction by principal a, 1 if by principal b.
    '''
    
    # note: I have little idea how the following code works.  It was
    # mostly copied from the previous paper's scripts.  Check there if
    # confused.
    float_princ_list = map(
        lambda princ_num : float(princ_num), principal_list)
    window = pylab.ones(10)/10.0
    rate = pylab.convolve(float_princ_list, window, 'same')


    _fairness_plot_set_defaults()
    plt.plot(rate, color='red')
    yticks = [-.1, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.1]
    ylabels = ['', '0%', '20%', '40%', '60%', '80%', '100%', '']

    plt.yticks(yticks, ylabels, fontsize=12)
    # plt.xticks(xtiks, xlabels, fontsize=7)
    plt.xlabel(xlabel, fontsize=16, verticalalignment='top')
    plt.ylabel(ylabel, fontsize=18)
    
    plt.savefig(output_filename)

    
def box_and_whisker_throughput(throughput_results_list,
                               xlabel, ylabel,output_filename):
    '''
    @param {list} throughput_results_list --- Each element is a
    ThroughputResult object.  List is sorted in ascending order.
    '''
    str_num_switches = map(
        lambda throughput_result : str(throughput_result.num_switches),
        throughput_results_list)
    throughput_data = map(
        lambda throughput_result :
            throughput_result.throughput_list_ks_per_second,
        throughput_results_list)

    _box_and_whisker_raw(
        str_num_switches,throughput_data,xlabel,ylabel,output_filename)


def box_and_whisker_latency(latency_results_list,
                            xlabel, ylabel,output_filename):
    '''
    @param {list} throughput_results_list --- Each element is a
    LatencyResult object.  List is sorted in ascending order.
    '''
    str_num_switches = map(
        lambda latency_result : str(latency_result.num_switches),
        latency_results_list)
    latency_data = map(
        lambda latency_result :
            latency_result.latency_list_ms,
        latency_results_list)

    _box_and_whisker_raw(
        str_num_switches,latency_data,xlabel,ylabel,output_filename)

def scatter(x_data,y_data,xlabel,ylabel,output_filename):
    '''
    @param {list} x_data --- A list of numbers
    
    @param {list} y_data --- A list of numbers.  Note len(x_data) must
    equal len(y_data)
    '''
    _scatter_plot_set_defaults()

    plt.scatter(x_data,y_data)
    plt.xlabel(xlabel, fontsize=16, verticalalignment='center')
    plt.ylabel(ylabel, fontsize=18)
    yticks = _create_y_ticks(max(y_data))
    plt.yticks(yticks, yticks,fontsize=12)
    
    plt.savefig(output_filename)

def hist(data,xlabel,output_filename):
    '''
    @param {list} data --- A list of numbers
    '''
    _hist_plot_set_defaults()
    plt.hist(data)
    plt.xlabel(xlabel, fontsize=18)
    plt.savefig(output_filename)

    
def bar_chart(conditions_data_list,conditions_legend_list,
              conditions_xtick_list,xlabel,ylabel,
              output_filename):
    '''
    @param {list} conditions_data_list --- Each element of
    conditions_data_list is a list of LatencyResult objects.  Eg.,

    [
      [ <LatRes1_a>, <LatRes1_b> ],    # condition 1
      [ <LatRes2_a>, <LatRes2_b> ]     # condition 2
      ...
    ]

    In the above case, the first list of LatencyResult objects
    corresponds to a single condition (eg., speculation on) and the
    second set of numbers corresponds to another condition (eg.,
    speculation off).  The length of each condition list should be the
    same.

    @param {list} conditions_legend_list --- Each element is a string,
    corresponding to the name of the condition in the legend.

    @param {list} conditions_xtick_list --- Each element is a string,
    corresponding to an x-axis label.
    '''
    _bar_chart_set_defaults()

    num_conditions = len(conditions_data_list)
    num_xs = len(conditions_data_list[0])
    ind = numpy.arange(num_xs)
    # the width of the bars
    width = 0.35
    
    rect_list = []
    
    # create a set of rectangles for each element in
    for i in range(0,num_conditions):

        # each element of condition_data_list is a LatencyResult
        # object
        condition_latency_result_list = conditions_data_list[i]

        # the average of each list of numbers in condition_data_list
        data_type_means_list = map(
            lambda latency_result : numpy.mean(latency_result.latency_list_ms),
            condition_latency_result_list)
        data_type_stddev_list = map(
            lambda latency_result : numpy.std(latency_result.latency_list_ms),
            condition_latency_result_list)
        
        color = BAR_CHART_COLOR_VEC[ i % len(BAR_CHART_COLOR_VEC)]
        rect = plt.bar(
            ind + i*width, data_type_means_list,
            width,color=color,yerr=data_type_stddev_list)
                
        rect_list.append(rect)

    # add labels/legends
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.xticks(ind+width,conditions_xtick_list,fontsize=12)

    plt.figlegend( rect_list, conditions_legend_list, loc='upper center')
    for i in range(0,num_conditions):
        _autolabel(plt,rect_list[i])

    plt.savefig(output_filename)


def _autolabel(ax,rects):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%.2f'%height,
                ha='center', va='bottom')

    
    
def _box_and_whisker_raw(xtick_list,data_list,xlabel,ylabel,output_filename):
    '''
    @param {list} xtick_list --- Each element is a string,
    corresponding to an x-label for each data type.

    @param {list} data_list --- Each element is a list containing
    floats.  Use these to produce a box and whisker for each x.

    @param {string} xlabel --- A label for the x axis

    @param {string} ylabel --- A label for the y axis
    '''
    _box_and_whisker_plot_set_defaults()
    bp = plt.boxplot(data_list,sym='',widths=.3)
    plt.setp(bp['medians'], color='#000000', lw=2)
    plt.setp(bp['boxes'], color='#808080', lw=1)
    plt.setp(bp['caps'], color='#f03030', lw=1)
    plt.setp(bp['whiskers'], color='#808080', lw=1, ls='-')

    medians = [numpy.median(d) for d in data_list]
    for i in range(0, len(medians)):
        plt.text(
            i+1.22, medians[i], str(round(medians[i],2)), fontsize=12,
            verticalalignment='center')

    # x-y labels
    plt.xlabel(xlabel, fontsize=16, verticalalignment='top')
    plt.ylabel(ylabel, fontsize=16, multialignment='center')

    # x-y ticks
    yticks = _create_y_ticks(max(max(data_list)))
    plt.yticks(yticks, map(str, yticks), fontsize=12)
    plt.xticks(numpy.arange(1, 2+len(xtick_list)), xtick_list, fontsize=12)

    plt.savefig(output_filename)    
    

def _create_y_ticks(max_y):

    ytikmax = int(math.ceil(max_y))
    if (ytikmax > 15):
        ytiks = [0, 5, 10, 15, 20]
    elif (ytikmax > 12):
        ytiks = [0, 5, 10, 15]
    elif (ytikmax > 10):
        ytiks = [0, 4, 8, 12]
    elif (ytikmax > 8):
        ytiks = [0, 2, 4, 6, 8, 10]
    elif (ytikmax > 5):
        ytiks = [0, 2, 4, 6, 8]
    elif (ytikmax > 4):
        ytiks = [0, 1, 2, 3, 4, 5]
    elif (ytikmax > 3):
        ytiks = [0, 1, 2, 3, 4]
    elif (ytikmax > 2):
        ytiks = [0, 1, 2, 3]
    elif (ytikmax > 1):
        ytiks = [0, 0.5, 1, 1.5, 2]
    else:
        ytiks = [0, 0.2, 0.4, 0.6, 0.8, 1]

    return ytiks

    
    
def _box_and_whisker_plot_set_defaults():
    plt.clf()
    fig = plt.figure(1)
    fig.set_size_inches(6, 2.5)
    plt.subplots_adjust(left=0.15, right=0.98, bottom=0.25, top=0.95)

def _bar_chart_set_defaults():
    # currently, bar chart defaults are same as box and whisker.
    _box_and_whisker_plot_set_defaults()
    
def _scatter_plot_set_defaults():
    # currently, scatter defaults are same as box and whisker.
    _box_and_whisker_plot_set_defaults()

def _hist_plot_set_defaults():
    # currently, hist defaults are same as box and whisker.
    _box_and_whisker_plot_set_defaults()
    
def _fairness_plot_set_defaults():
    # currently, fairness defaults are same as box and whisker.
    _box_and_whisker_plot_set_defaults()
    # The last digit of the 2000 x label was cut off with right=0.98
    plt.subplots_adjust(left=0.15, right=0.96, bottom=0.25, top=0.95)
