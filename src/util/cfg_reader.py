import json

def read_config(config_filename):
    '''
    Arguments:
      config_filename: {String} The name of the config file to read.

    Returns:
      {dictionary} --- Nested dictionary that contains configuration
      parameters.  What to run, what to name output, and where to get
      experimental data from.
    '''
    with open(config_filename,'r') as fd:
        return json.loads(fd.read())
