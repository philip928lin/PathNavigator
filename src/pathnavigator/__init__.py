import math
from .pathnavigator import PathNavigator

# A factory function for common use cases. This reduces the cognitive 
# load for new users who may not be familiar with your class.

def create(root_dir: str = None, max_depth: int = math.inf, max_files: int = math.inf, max_folders: int = math.inf) -> PathNavigator:
    """
    Create a PathNavigator object with the given root directory and load nested directories.
    
    Parameters
    ----------
    root_dir : str
        The root directory to manage. If it is not given, we use the current working
        directory and load_nested_dirs will be set to False.
    max_depth : int
        The maximum depth to load the nested directories. Default is math.inf.
    max_files : int
        The maximum number of files to load. Default is math.inf.
    max_folders : int
        The maximum number of subdirectories to load. Default is math.inf.
        
    Returns
    -------
    PathNavigator
        The PathNavigator object with the given root directory.
    """
    return PathNavigator(root_dir=root_dir, max_depth=max_depth, max_files=max_files, max_folders=max_folders)