import logging
import inspect

# Basic log configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Function that returns a logger with the caller module's name
def get_logger():
    # Get the caller's stack frame (who called this function)
    caller_frame = inspect.stack()[1]
    # Get the caller's module
    caller_module = inspect.getmodule(caller_frame[0])
    # Return a logger with the module name
    return logging.getLogger(caller_module.__name__)