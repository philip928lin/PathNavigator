import math
from pathlib import Path
from .folder import Folder
from .shortcut import Shortcut

class PathNavigator(Folder):
    """
    A class to manage the root folder and recursively load its nested structure (subfolders and files).
        
    Examples
    --------
    >>> pn = PathNavigator('/path/to/root')

    >>> pn.folder1.get()        # returns the full path to folder1 as a Path object.
    >>> pn.folder1.get_str()    # returns the full path to folder1 as a string.
    >>> pn.folder1.get("file.txt")        # returns the full path to file.txt as a Path object.
    >>> pn.get("folder1")       # returns the full path to folder1 as a Path object.
    >>> pn.folder1.get_str("file.txt")    # returns the full path to file.txt as a string.

    >>> pn.folder1.set_sc('my_folder')  # set the shortcut to folder1 which can be accessed by pn.sc.my_folder or pn.sc.get("my_folder") or pn.sc.get_str("my_folder").
    >>> pn.folder1.set_sc('my_file', 'file.txt')  # set the shortcut to file.txt which can be accessed by pn.sc.my_file or pn.sc.get("my_file") or pn.sc.get_str("my_file").
    >>> pn.sc.add('shortcut_name', 'shortcut_path')    # add a customized shortcut independent to pn internal folder structure.

    >>> pn.folder1.ls()         # prints the contents (subfolders and files) of folder1.
    >>> pn.tree()               # prints the entire nested folder structure.
    
    >>> pn.folder1.chdir()      # change the current directory to folder1.
    >>> pn.folder1.add_to_sys_path()    # add folder1 to the system path.
    
    >>> pn.exists('folder1')    # check if folder1 exists in the folder structure.
    >>> pn.folder1.listdirs()   # returns a list of subfolders in folder1.
    >>> pn.folder1.listfiles()  # returns a list of files in folder1.

    >>> pn.mkdir('folder1', 'folder2')  # make a subfolder under the root. In this case, 'root/folder1/folder2' will be created.
    >>> pn.remove('folder1')    # removes a file or subfolder from the folder and deletes it from the filesystem.
    """
    
    def __init__(self, root_dir: str = None, max_depth: int = math.inf, max_files: int = math.inf, max_folders: int = math.inf, display: bool = False):
        """
        Initialize the PathNavigator object with the given root directory and load nested directories.
        
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
        display : bool
            Whether to display action complete info like changing directory. Default is False.
            
        Returns
        -------
        PathNavigator
            The PathNavigator object with the given root directory.
        """
        if root_dir is None:
            root_dir = Path.cwd()

        self._pn_root = Path(root_dir)
        self._pn_max_depth = max_depth
        self._pn_max_files = max_files
        self._pn_max_folders = max_folders
        self._pn_display = display
        self.sc = Shortcut()  # Initialize Shortcut manager as an attribute
        super().__init__(name=self._pn_root.name, parent_path=self._pn_root.parent, _pn_object=self)
        
        self.scan(max_depth=max_depth, max_files=max_files, max_folders=max_folders)

    def __str__(self):
        return str(self._pn_root)

    def __repr__(self):
        return f"PathNavigator({self._pn_root})"
    
    def __call__(self):
        return self._pn_root


    
    
