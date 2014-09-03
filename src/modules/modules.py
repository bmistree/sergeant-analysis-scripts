# Keys are strings, values are functions for processing data.  When we
# encounter a key in our dictionary from reading the config file, the
# value of the key are the arguments that get passed to the function.
_available_processor = {}
def register_processor(cls):
    global available_proceses
    _available_processor[cls.NAME] = cls
    
def get_processor(processor_name):
    return _available_processor.get(processor_name,None)
