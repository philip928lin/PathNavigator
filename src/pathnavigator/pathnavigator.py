import os

from .folder import Folder
from .shortcut import Shortcut

class PathNavigator(Folder):
    """
    A class to manage the root folder and recursively load its nested structure (subfolders and files).
    
    
    dir()
        Returns the full path to this folder.
    ls()
        Prints the contents (subfolders and files) of the folder.
    remove(name)
        Removes a file or subfolder from the folder and deletes it from the filesystem.
    mkdir(*args)
        Creates a subdirectory in the current folder and updates the internal structure.

    Methods
    -------
    reload()
        Reloads the entire folder structure from the filesystem.
        
    Examples
    --------
    >>> pn = PathNavigator('/path/to/root')
    >>> pn.mkdir('folder1', 'folder2')     # make a subfolder under the root
    >>> pn.folder1.dir()        # returns the full path to folder1.
    >>> pn.folder1.ls()         # prints the contents (subfolders and files) of folder1.
    >>> pn.folder1.file1        # returns the full path to file1.
    >>> pn.remove('folder1')    # removes a file or subfolder from the folder and deletes it from the filesystem.
    """
    
    def __init__(self, root_dir: str, load_nested_directories=True):
        """
        Initialize the PathNavigator with the root directory and create a Shortcut manager.

        Parameters
        ----------
        root_dir : str
            The root directory to manage.
        load_nested_directories : bool, optional
            Whether to load nested directories and files from the filesystem. Default is True.
        """
        self._pn_root = root_dir
        self.sc = Shortcut()  # Initialize Shortcut manager as an attribute
        super().__init__(name=os.path.basename(self._pn_root), parent_path=os.path.dirname(self._pn_root), _pn_object=self)
        if load_nested_directories:
            self._pn_load_nested_directories(self._pn_root, self)
        self.display(show_files=False)

    def _pn_load_nested_directories(self, current_path: str, current_folder: Folder):
        """
        Recursively load subfolders and files from the filesystem into the internal structure.

        Parameters
        ----------
        current_path : str
            The current path to load.
        current_folder : Folder
            The Folder object representing the current directory.
        """
        for entry in os.scandir(current_path):
            if entry.is_dir():
                folder_name = entry.name
                valid_folder_name = current_folder._pn_converter.to_valid_name(folder_name)
                new_subfolder = Folder(folder_name, parent_path=current_path, _pn_object=self)
                current_folder.subfolders[valid_folder_name] = new_subfolder
                self._pn_load_nested_directories(entry.path, new_subfolder)
            elif entry.is_file():
                file_name = entry.name
                valid_filename = current_folder._pn_converter.to_valid_name(file_name)
                current_folder.files[valid_filename] = entry.path
    
    def reload(self):
        """
        Reload the entire folder structure from the root directory.

        Examples
        --------
        >>> pn = PathNavigator('/path/to/root')
        >>> pn.reload()
        """
        self._pn_load_nested_directories(self._pn_root, self)


    
    
