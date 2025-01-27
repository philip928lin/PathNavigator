from .pathnavigator import PathNavigator

# A factory function for common use cases. This reduces the cognitive 
# load for new users who may not be familiar with your class.

def create(root_dir: str = None, load_nested_dirs: bool = True, auto_reload: bool = True) -> PathNavigator:
    """
    Create a PathNavigator object with the given root directory and load nested directories.

    Parameters
    ----------
    root_dir : str
            The root directory to manage. If it is not given, we use the current working
            directory and load_nested_dirs will be set to False.
    load_nested_dirs : bool, optional
        Whether to load nested directories and files from the filesystem. Default is True.
    auto_reload : bool, optional
        Whether to automatically reload the folder structure when using exists(), 
        get(), get_str(), mkdir(), and set_sc(). Default is True.

    Returns
    -------
    PathNavigator
        The PathNavigator object with the given root directory.
    """
    return PathNavigator(root_dir, load_nested_dirs, auto_reload)