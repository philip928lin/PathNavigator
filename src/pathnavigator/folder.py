import os
import sys
import re
import math
import shutil
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Any
from itertools import islice
from .att_name_convertor import AttributeNameConverter

"""
    Methods
    -------
    __getattr__(item)
        Allows access to subfolders and files as attributes. Replaces '_' with spaces.
    scan(max_depth=math.inf, max_files=math.inf, max_folders=math.inf, include=None, exclude=None, _only_folders=False, _only_files=False, _depth_count=0, _clear=True)
        Recursively scans subfolders and files in the current folder.
    ls()
        Prints the contents (subfolders and files) of the folder.
    get()
        Get the full path of a file in the current folder.
    get_str()
        Get the full path str of a file in the current folder.
    join(*args)
        Joins the current folder path with additional path components.
    set_sc(name, filename=None)
        Adds a shortcut to this folder (or file) using the Shortcut manager.
    remove(name)
        Removes a file or subfolder from the folder and deletes it from the filesystem.
    mkdir(*args)
        Creates a subdirectory in the current folder and updates the internal structure.
    exists(name, scan_before_checking=False)
        Checks if a file or subfolder exists in the current folder.
    set_all_files_to_sc(overwrite=False, prefix="")
        Adds all files in the current folder to the shortcut manager.
    list(mode='name', type=None)
        Lists subfolders or files in the current folder based on the specified filters.
    add_to_sys_path(method='insert', index=1)
        Adds the directory to the system path.
    chdir()
        Sets this directory as the working directory.
    tree(level=-1, limit_to_directories=False, length_limit=1000, level_length_limit=1000)
        Prints a visual tree structure of the folder and its contents.
"""

@dataclass
class Folder:
    """
    A class to represent a folder in the filesystem and manage subfolders and files.

    Attributes
    ----------
    name : str
        The name of the folder.
    parent_path : str
        The path of the parent folder.
    subfolders : dict
        A dictionary of subfolder names (keys) and Folder objects (values).
    files : dict
        A dictionary of file names (keys) and their paths (values).
    _pn_object : object
        The PathNavigator object that this folder belongs to.
    _pn_converter : object
        The AttributeNameConverter object for converting attribute names.
    """

    name: str           # Folder name
    parent_path: Path   # Track the parent folder path for constructing full paths
    subfolders: Dict[str, Any] = field(default_factory=dict)
    files: Dict[str, str] = field(default_factory=dict)
    _pn_object: object = field(default=None)
    _pn_converter: object = field(default_factory=lambda: AttributeNameConverter())
    _pn_current_depth: int = field(default=0)

    def __getattr__(self, item):
        """
        Access subfolders and files as attributes.

        Parameters
        ----------
        item : str
            The name of the folder or file, replacing spaces with underscores.

        Returns
        -------
        Folder or str
            Returns the Folder object or file path.

        Raises
        ------
        AttributeError
            If the folder or file does not exist.

        Examples
        --------
        >>> folder = Folder(name="root")
        >>> folder.subfolders['sub1'] = Folder("sub1")
        >>> folder.files['file1'] = "/path/to/file1"
        >>> folder.sub1
        Folder(name='sub1', parent_path='', subfolders={}, files={})
        >>> folder.file1
        '/path/to/file1'
        """
        #folder_name = item.replace('_', ' ')
        #if folder_name in self.subfolders:
        #    return self.subfolders[folder_name]
        #elif item in self.subfolders:
        #    return self.subfolders[item]

        if item in self.subfolders:
            return self.subfolders[item]
        if item in self.files:
            return self.files[item]
        raise AttributeError(f"'{item}' not found in folder '{self.name}'")

    def scan(self, max_depth: int = math.inf, max_files: int = math.inf, max_folders: int = math.inf,
             include: str = None, exclude: str = None,
             _only_folders: bool = False, _only_files: bool = False,
             _depth_count: int = 0, _clear: bool = True):
        """
        Recursively scan subfolders and files in the current folder.

        Parameters
        ----------
        max_depth : int, optional
            The maximum depth to scan. Default is math.inf.
        max_files : int, optional
            The maximum number of files to scan. Default is math.inf.
        max_folders : int, optional
            The maximum number of subfolders to scan. Default is math.inf.
        include : str, optional
            A regex pattern to include files or folders matching the pattern.
            Default is None (include all).
        exclude : str, optional
            A regex pattern to exclude files or folders matching the pattern.
            Default is None (exclude none).
        _only_folders : bool, optional
            Whether to scan only subfolders. Default is False.
        _only_files : bool, optional
            Whether to scan only files. Default is False.
        _depth_count : int, optional
            The current depth count. Default is 0.
        _clear : bool, optional
            Whether to clear the subfolders and files before scanning. Default is True.
        """
        self._pn_current_depth = _depth_count
        if _depth_count >= max_depth:
            #print(f"Depth limit reached: {max_depth}")
            return None

        if _clear:
            # Clear the subfolders and files before scanning
            self.subfolders.clear()
            self.files.clear()
        # Else, continue scanning from the current state

        _folder_count = 0
        _file_count = 0

        include_pattern = re.compile(include) if include else None
        exclude_pattern = re.compile(exclude) if exclude else None

        for entry in self.get().iterdir():
            entry_name = entry.name

            if exclude_pattern and exclude_pattern.search(entry_name):
                continue  # Skip excluded files or folders

            if include_pattern and not include_pattern.search(entry_name):
                continue  # Skip non-matching entries if include is specified

            if entry.is_dir() and not _only_files:
                if _folder_count < max_folders:
                    valid_folder_name = self._pn_converter.to_valid_name(entry_name)
                    new_subfolder = Folder(entry_name, parent_path=self.get(), _pn_object=self._pn_object)
                    self.subfolders[valid_folder_name] = new_subfolder
                    # Recursively scan subfolders
                    new_subfolder.scan(
                        max_depth=max_depth,
                        max_files=max_files,
                        max_folders=max_folders,
                        _depth_count=_depth_count+1
                        )
                    _folder_count += 1
                else:
                    #print(f"Maximum number of folders reached: {max_folders}")
                    pass
            elif entry.is_file() and not _only_folders:
                if _file_count < max_files:
                    valid_filename = self._pn_converter.to_valid_name(entry_name)
                    self.files[valid_filename] = entry
                    _file_count += 1
                else:
                    #print(f"Maximum number of files reached: {max_files}")
                    pass


    def ls(self):
        """
        Print the contents of the folder, including subfolders and files.

        Prints subfolders first, followed by files.

        Examples
        --------
        >>> folder = Folder(name="root")
        >>> folder.subfolders['sub1'] = Folder("sub1")
        >>> folder.files['file1'] = "/path/to/file1"
        >>> folder.ls()
        Contents of '/root':
        Subfolders:
          [Dir] sub1
        Files:
          [File] file1
        """
        print(f"Contents of '{self.get()}':")
        print("(-> represent the attribute name used to access the subfolder or file.)")
        if self.subfolders:
            print("Subfolders:")
            for subfolder in self.subfolders:
                org_name = self._pn_converter.get(subfolder)
                if self._pn_converter._pn_is_valid_attribute_name(org_name) is False:
                    print(f"  [Dir] {org_name}\n         -> {subfolder}")
                else:
                    print(f"  [Dir] {org_name}")
        else:
            print("No subfolders.")

        if self.files:
            print("Files:")
            for file in self.files:
                org_name = self._pn_converter.get(file)
                if self._pn_converter._pn_is_valid_attribute_name(org_name) is False:
                    print(f"  [File] {org_name}\n         -> {file}")
                else:
                    print(f"  [File] {org_name}")
        else:
            print("No files.")

    def remove(self, name: str):
        """
        Remove a file or subfolder from the folder and delete it from the filesystem.

        Parameters
        ----------
        name : str
            The name of the file or folder to remove, replacing underscores with spaces if needed.

        Examples
        --------
        >>> folder = Folder(name="root")
        >>> folder.subfolders['sub1'] = Folder("sub1")
        >>> folder.files['file1'] = "/path/to/file1"
        >>> folder.remove('sub1')
        Subfolder 'sub1' has been removed from '/root'
        >>> folder.remove('file1')
        File 'file1' has been removed from '/root'
        """
        _pn_object = self._pn_object
        valid_name = self._pn_converter.to_valid_name(name)
        org_name = self._pn_converter.get(valid_name)

        if valid_name not in self.subfolders and valid_name not in self.files:
            self.scan(
            max_depth=_pn_object._pn_max_depth-self._pn_current_depth,
            max_files=_pn_object._pn_max_files,
            max_folders=_pn_object._pn_max_folders,
            )
        if valid_name in self.subfolders:
            full_path = self.join(org_name)
            shutil.rmtree(full_path)
            del self.subfolders[valid_name]
            self.scan(
            max_depth=_pn_object._pn_max_depth-self._pn_current_depth,
            max_files=_pn_object._pn_max_files,
            max_folders=_pn_object._pn_max_folders,
            _only_files=False,
            _only_folders=True
            )
            print(f"Subfolder '{org_name}' has been removed from '{self.get()}'")

        elif valid_name in self.files:
            self.scan(
            max_depth=_pn_object._pn_max_depth-self._pn_current_depth,
            max_files=_pn_object._pn_max_files,
            max_folders=_pn_object._pn_max_folders,
            _only_files=True,
            _only_folders=False
            )
            full_path = self.files[valid_name]
            os.remove(full_path)
            del self.files[valid_name]
            print(f"File '{org_name}' has been removed from '{self.get()}'")
        else:
            print(f"'{name}' not found in '{self.get()}'")

        # Rescan the folder structure after removing a file or subfolder

    def join(self, *args) -> str:
        """
        Join the current folder path with additional path components.

        Parameters
        ----------
        args : str
            Path components to join with the current folder path.

        Returns
        -------
        str
            The full path after joining the current folder path with the provided components.

        Examples
        --------
        >>> folder = Folder(name="root")
        >>> folder.join("subfolder", "file.txt")
        '/home/user/root/subfolder/file.txt'
        """
        return self.get().joinpath(*args)

    def mkdir(self, *args):
        """
        Create a directory inside the current folder and update the internal structure.

        Parameters
        ----------
        args : str
            Path components for the new directory relative to the current folder.

        Examples
        --------
        >>> folder = Folder(name="root")
        >>> folder.mkdir("new_subfolder")
        >>> folder.subfolders['new_subfolder']
        Folder(name='new_subfolder', parent_path='/root', subfolders={}, files={})
        """
        full_path = self.join(*args) #os.path.join(self.get(), *args)
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"Created directory '{full_path}'")

        # Rescan the folder structure after creating a new subfolder
        _pn_object = self._pn_object
        self.scan(
            max_depth=_pn_object._pn_max_depth-self._pn_current_depth,
            max_files=_pn_object._pn_max_files,
            max_folders=_pn_object._pn_max_folders,
            )

    def exists(self, name: str, scan_before_checking=False) -> bool:
        """
        Check if a file or subfolder exists in the current folder.

        Parameters
        ----------
        name : str, optional
            The name of the file or subfolder to check.

        Returns
        -------
        bool
            True if the file or folder exists, False otherwise.

        Examples
        --------
        >>> folder = Folder(name="root")
        >>> folder.exists("filename_or_foldername")
        False
        """
        if scan_before_checking:
            # Rescan the folder structure before checking if a file or subfolder exists
            _pn_object = self._pn_object
            self.scan(
                max_depth=_pn_object._pn_max_depth-self._pn_current_depth,
                max_files=_pn_object._pn_max_files,
                max_folders=_pn_object._pn_max_folders,
                )
        return os.path.exists(self.get() / name)

    def set_sc(self, name: str, filename: str = None):
        """
        Add a shortcut to this folder using the Shortcut manager.

        Parameters
        ----------
        name : str
            The name of the shortcut to add.
        filename : str, optional
            The name of the file to add a shortcut for. Default is None.

        Examples
        --------
        >>> folder = Folder(name="root")
        >>> folder.set_sc("my_folder")
        Shortcut 'my_folder' added for path '/root'
        """
        if filename is None:
            self._pn_object.sc.add(name, self.get())
        else:
            valid_name = self._pn_converter.to_valid_name(filename)
            if valid_name not in self.files:
                # Rescan the folder to confirm the existence of the file before raising an error
                _pn_object = self._pn_object
                self.scan(
                    max_depth=_pn_object._pn_max_depth-self._pn_current_depth,
                    max_files=_pn_object._pn_max_files,
                    max_folders=_pn_object._pn_max_folders,
                    _only_files=True
                    )
            if valid_name not in self.files:
                raise ValueError(
                    f"'{filename}' not found in '{self.get()}'." +
                    " Try to re-scan the pn object by pn.scan() if the file exist in the file system."
                    )
            self._pn_object.sc.add(name, self.files[valid_name])

    def set_all_files_to_sc(self, overwrite: bool = False, prefix: str = ""):
        """
        Add all files in the current folder to the shortcut manager.

        Parameters
        ----------
        overwrite : bool, optional
            Whether to overwrite existing shortcuts. Default is False.
        prefix : str, optional
            The prefix to add to the shortcut names. Default is "".
        """

        self._pn_object.sc.add_all_files(directory=self.get(), overwrite=overwrite, prefix=prefix)

    def get(self, *args) -> Path:
        """
        Get the full path of a file or a subfolder in the current folder.
        
        Parameters
        ----------
        *args : str
            The name of the file or the subfolder to get. If None, returns the full path
            of the current folder. Default is None.
            
        Returns
        -------
        Path
            The full path to the file or the subfolder.
        """
        # If no arguments are provided, return the path of the current folder
        if not args:
            return Path(self.parent_path) / self.name


        # Otherwise, process the parts in args
        path = Path(*args)
        current_obj = self
        for i, part in enumerate(path.parts):
            valid_name = self._pn_converter.to_valid_name(part)

            if i == len(path.parts) - 1:
                if valid_name not in current_obj.files and valid_name not in current_obj.subfolders:
                    # Rescan the folder to confirm the existence of the file before raising an error
                    _pn_object = current_obj._pn_object
                    current_obj.scan(
                        max_depth=_pn_object._pn_max_depth-self._pn_current_depth,
                        max_files=_pn_object._pn_max_files,
                        max_folders=_pn_object._pn_max_folders,
                        )
                if valid_name not in current_obj.files and valid_name not in current_obj.subfolders:
                    raise ValueError(
                        f"'{path}' not found in '{Path(self.parent_path) / self.name}'." +
                        " Try to re-scan the pn object by pn.scan() if the file exist in the file system."
                        )
                return Path(current_obj.parent_path) / current_obj.name / part
            else:
                if valid_name not in current_obj.subfolders:
                    # Rescan the folder to confirm the existence of the file before raising an error
                    _pn_object = current_obj._pn_object
                    current_obj.scan(
                        max_depth=_pn_object._pn_max_depth-self._pn_current_depth,
                        max_files=_pn_object._pn_max_files,
                        max_folders=_pn_object._pn_max_folders,
                        )
                if valid_name not in current_obj.subfolders:
                    raise ValueError(
                        f"'{part}' not found in '{Path(current_obj.parent_path) / current_obj.name}'." +
                        " Try to re-scan the pn object by pn.scan() if the file exist in the file system."
                        )
                current_obj = current_obj.subfolders[valid_name]

    def get_str(self, *args) -> str:
        """
        Get the full path of a file or a subfolder in the current folder.

        Parameters
        ----------
        fname : str
            The name of the file or the subfolder to get. If None, returns the full path
            of the folder. Default is None.

        Returns
        -------
        str
            The full path to the file or the subfolder.

        Examples
        --------
        >>> folder = Folder(name="root")
        >>> folder.get_str("file1")
        '/home/user/root/file1'
        """
        return str(self.get(*args))

    def list(self, mode='name', type=None):
        """
        List subfolders or files in the current folder.

        Parameters
        ----------
        mode : str, optional
            The mode to use for listing items. Options are 'name' (default), 'dir', and 'stem'.
            - 'name': List item names (with extensions for files).
            - 'dir': List full item paths.
            - 'stem': List file stems (filenames without extensions).
        type : str, optional
            The type of items to list. Options are:
            - 'folder': List only folders.
            - 'file': List only files.
            - None (default): List both files and directories.

        Returns
        -------
        list
            A list of directories or files (or both) based on the specified filters.
        """
        mode_map = {
            'name': lambda item: item.name,
            'dir': lambda item: item,
            'stem': lambda item: item.stem
        }

        items = self.get().iterdir()  # Get all items in the folder

        if type == 'folder':
            items = (item for item in items if item.is_dir())  # Filter only directories
        elif type == 'file':
            items = (item for item in items if item.is_file())  # Filter only files

        return [mode_map[mode](item) for item in items]

    def chdir(self):
        """
        Set this directory as working directory.

        Examples
        --------
        >>> folder.chdir()
        """
        os.chdir(self.get())
        print(f"Changed working directory to '{self.get()}'")

    def add_to_sys_path(self, method='insert', index=1):
        """
        Adds the directory to the system path.

        Parameters
        ----------
        method : str, optional
            The method to use for adding the path to the system path.
            Options are 'insert' (default) or 'append'.
        index : int, optional
            The index at which to insert the path if method is 'insert'.
            Default is 1.

        Raises
        ------
        ValueError
            If the method is not 'insert' or 'append'.

        Examples
        --------
        >>> folder = Folder('/path/to/folder')
        >>> folder.add_to_sys_path()
        Inserted /path/to/folder at index 1 in system path.

        >>> folder.add_to_sys_path(method='append')
        Appended /path/to/folder to system path.

        >>> folder.add_to_sys_path(method='invalid')
        Invalid method: invalid. Use 'insert' or 'append'.
        """
        if self.get() not in sys.path:
            if method == 'insert':
                sys.path.insert(index, self.get())
                print(f"Inserted {self.get()} at index {index} in system path.")
            elif method == 'append':
                sys.path.append(self.get())
                print(f"Appended {self.get()} to system path.")
            else:
                print(f"Invalid method: {method}. Use 'insert' or 'append'.")
        else:
            print(f"{self.get()} is already in the system path.\n Current system paths:\n{sys.path}")

    def tree(self, level: int=-1, limit_to_directories: bool=False,
            length_limit: int=1000, level_length_limit: int=100):
        """
        Print a visual tree structure of the folder and its contents.

        Parameters
        ----------
        level : int, optional
            The max_depth of the tree to print. Default is -1 (print all levels).
        limit_to_directories : bool, optional
            Whether to limit the tree to directories only. Default is False.
        length_limit : int, optional
            The maximum number of lines to print. Default is 1000.
        level_length_limit : int, optional
            The maximum number of lines to print per level. Default is 100.
        """
        space = '    '
        branch = '│   '
        tee = '├── '
        last = '└── '

        dir_path = self.get()
        files = 0
        directories = 0

        def inner(folder: Folder, prefix: str='', level=-1):
            nonlocal files, directories
            if not level:
                return  # 0, stop iterating

            subfolder_pointers = [tee] * (len(folder.subfolders) - 1) + [last]
            if folder.files:
                subfolder_pointers[-1] = tee

            for i, (pointer, subfolder) in enumerate(zip(subfolder_pointers, folder.subfolders.values())):
                if i == level_length_limit:
                    yield prefix + pointer + f"...limit reached (total: {len(folder.subfolders)} subfolders)"
                elif i > level_length_limit:
                    pass
                else:
                    yield prefix + pointer + subfolder.get().name
                    directories += 1
                    extension = branch if pointer == tee else space
                    yield from inner(subfolder, prefix=prefix + extension, level=level - 1)

            if not limit_to_directories:
                file_pointers = [tee] * (len(folder.files) - 1) + [last]
                for i, (pointer, filepath) in enumerate(zip(file_pointers, folder.files.values())):
                    if i == level_length_limit:
                        yield prefix + pointer + "...limit reached (total: {len(folder.files)} files)"
                    elif i > level_length_limit:
                        pass
                    else:
                        yield prefix + pointer + filepath.name
                        files += 1

        print(dir_path.name)
        iterator = inner(self, level=level)
        for line in islice(iterator, length_limit):
            print(line)
        if next(iterator, None):
            print(f'... length_limit, {length_limit}, reached, counted:')
        print(f'\n{directories} directories' + (f', {files} files' if files else ''))
