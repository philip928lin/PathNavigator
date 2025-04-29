import getpass
import platform
import math
from pathlib import Path
from .pathnavigator import *
from .folder import *
from .shortcut import *

# A factory function for common use cases. This reduces the cognitive 
# load for new users who may not be familiar with your class.

def create(
    root_dir: str = None, 
    max_depth: int = math.inf, 
    only_include: list = [], only_exclude: list = [],
    only_folders: bool = True, only_files: bool = False,
    max_files: int = math.inf, max_folders: int = math.inf,
    recursive_include_and_exclude: bool = False,
    display: bool = False
    ) -> PathNavigator:
    """
    Create a PathNavigator object with the given root directory and load nested directories. 
    Default to scan the tree of directories. Files will be dynamically added when 
    related methods are called, e.g., `get()`. This will avoid long initial loading time.
    
    Parameters
    ----------
    root_dir : str
        The root directory to manage. If it is not given, we use the current working
        directory and load_nested_dirs will be set to False.
    max_depth : int, optional
        The maximum depth to scan. Default is math.inf.
    only_include : list, optional
        A list of  patterns to include only files or folders that match the patterns.
        No `**` wildcard is allowed, only `*` is allowed.
    only_exclude : list, optional
        A list of patterns to exclude files or folders that match the patterns.
        No `**` wildcard is allowed, only `*` is allowed.
    only_folders : bool, optional
        Whether to scan only subfolders. Default is True.
        File will be dynamically added when related methods are called, e.g., `get()`.
    only_files : bool, optional
        Whether to scan only files. Default is False.
    max_files : int, optional
        The maximum number of files at each level to scan. Default is math.inf.
    max_folders : int, optional
        The maximum number of subfolders at each level to scan. Default is math.inf.
    recursive_include_and_exclude : bool, optional
            Whether to apply the include and exclude patterns recursively. Default is True.
    display : bool
        Whether to display action complete info like changing directory. Default is False.
        
    Returns
    -------
    PathNavigator
        The PathNavigator object with the given root directory.
    """
    return PathNavigator(
        root_dir=root_dir, 
        max_depth=max_depth, 
        only_include=only_include, only_exclude=only_exclude,
        only_folders=only_folders, only_files=only_files,
        max_files=max_files, max_folders=max_folders,
        recursive_include_and_exclude=recursive_include_and_exclude,
        display=display
        )

# Other info 
user = getpass.getuser()
os_name = platform.system()
#'Windows' for Windows
#'Linux' for Linux
#'Darwin' for macOS
