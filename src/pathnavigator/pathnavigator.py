import os
import sys
import json
import shutil
import re
import keyword
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class AttributeNameConverter:
    _pn_org_to_valid_name: dict = field(default_factory=dict)
    _pn_valid_name_to_org: dict = field(default_factory=dict)

    def to_valid_name(self, name: str) -> str:
        """Convert the original name to a valid attribute name."""
        if self._pn_is_valid_attribute_name(name) is False:
            valid_name = self._pn_convert_to_valid_attribute_name(name)
            print(f"Converting '{name}' to a valid attribute name, '{valid_name}'.")
            return valid_name
        else:
            return name

    def get(self, name: str) -> str:
        """Get the valid attribute name for the given original name."""
        if self._pn_needs_name_mapping(name):
            return self._pn_valid_name_to_org[name]
        else:
            return name
        
    def _pn_is_valid_attribute_name(
            self, name: str, 
            invalid_list=["sc", "reload", "dir", "ls", "remove", "join", "get",
                          "mkdir", "set_shortcut", "chdir", "add_to_sys_path", 
                          "name", "parent_path", "subfolders", "files"]
            ) -> bool:
        """Check if a given attribute name is valid."""
        if name.startswith('_pn_'):
            raise ValueError(f"Strings starting with '_pn_' are reserved in PathNavigator. Please modify '{name}' to eligible naming.")
        return name.isidentifier() and not keyword.iskeyword(name) and not name in invalid_list

    def _pn_convert_to_valid_attribute_name(self, name: str) -> str:
        """Convert ineligible attribute name to a valid one."""
        # Replace invalid characters (anything not a letter, digit, or underscore) with underscores
        valid_name = re.sub(r'\W|^(?=\d)', '_', name)  # \W matches non-word characters, ^(?=\d) ensures no starting digit
        
        # Ensure the name starts with an underscore
        if not valid_name.startswith('_'):
            valid_name = '_' + valid_name
        
        # Check if the converted name is a Python keyword and append an underscore if necessary
        if keyword.iskeyword(valid_name):
            valid_name += '_'
        
        # Store the mapping of ineligible to eligible names
        self._pn_org_to_valid_name[name] = valid_name
        self._pn_valid_name_to_org[valid_name] = name
        
        return valid_name

    def _pn_get_name_mapping(self):
        """Return the dictionary that maps ineligible names to eligible names."""
        return self._pn_org_to_valid_name

    def _pn_needs_name_mapping(self, name: str) -> bool:
        """Check if the original name needs to use the name mapping."""
        return name in self._pn_valid_name_to_org
    
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

    Methods
    -------
    __getattr__(item)
        Allows access to subfolders and files as attributes. Replaces '_' with spaces.
    dir()
        Returns the full path to this folder.
    ls()
        Prints the contents (subfolders and files) of the folder.
    join(*args)
        Joins the current folder path with additional path components.
    set_shortcut(name, filename=None)
        Adds a shortcut to this folder (or file) using the Shortcut manager.
    remove(name)
        Removes a file or subfolder from the folder and deletes it from the filesystem.
    mkdir(*args)
        Creates a subdirectory in the current folder and updates the internal structure.
    add_to_sys_path(method='insert', index=1)
        Adds the directory to the system path.
    """
    
    name: str
    parent_path: str = ""  # Track the parent folder path for constructing full paths
    _pn_object: object = field(default=None)
    subfolders: Dict[str, Any] = field(default_factory=dict)
    files: Dict[str, str] = field(default_factory=dict)
    _pn_converter: object = field(default_factory=lambda: AttributeNameConverter())

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

    def dir(self):
        """
        Get the full path of this folder.

        Returns
        -------
        str
            The full path to the folder.

        Examples
        --------
        >>> folder = Folder(name="root", parent_path="/home/user")
        >>> folder.dir()
        '/home/user/root'
        """
        return os.path.join(self.parent_path, self.name)

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
        print(f"Contents of '{self.dir()}':")
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
        valid_name = self._pn_converter.to_valid_name(name)
        org_name = self._pn_converter.get(valid_name)
        if valid_name in self.subfolders:
            full_path = self.join(org_name)
            shutil.rmtree(full_path)
            del self.subfolders[valid_name]
            print(f"Subfolder '{org_name}' has been removed from '{self.dir()}'")
        elif valid_name in self.files:
            full_path = self.files[valid_name]
            os.remove(full_path)
            del self.files[valid_name]
            print(f"File '{org_name}' has been removed from '{self.dir()}'")
        else:
            print(f"'{name}' not found in '{self.dir()}'")

        """
        clean_name_with_spaces = name.replace('_', ' ')
        clean_name_with_underscores = name.replace(' ', '_')
        
        if clean_name_with_underscores in self.subfolders:
            full_path = os.path.join(self.dir(), self.subfolders[clean_name_with_underscores].name)
            shutil.rmtree(full_path)
            del self.subfolders[clean_name_with_underscores]
            print(f"Subfolder '{clean_name_with_spaces}' has been removed from '{self.dir()}'")
        elif clean_name_with_underscores in self.files:
            full_path = self.files[clean_name_with_underscores]
            os.remove(full_path)
            del self.files[clean_name_with_underscores]
            print(f"File '{clean_name_with_spaces}' has been removed from '{self.dir()}'")
        else:
            print(f"'{clean_name_with_spaces}' not found in '{self.dir()}'")
        """

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
        return os.path.join(self.dir(), *args)

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
        full_path = self.join(*args) #os.path.join(self.dir(), *args)
        os.makedirs(full_path, exist_ok=True)

        relative_path = os.path.relpath(full_path, self.dir())
        path_parts = relative_path.split(os.sep)

        current_folder = self
        for part in path_parts:
            #clean_part = part.replace(' ', '_')
            valid_name = self._pn_converter.to_valid_name(part)
            if valid_name not in current_folder.subfolders:
                new_folder = Folder(part, parent_path=current_folder.dir())
                current_folder.subfolders[valid_name] = new_folder
            current_folder = current_folder.subfolders[valid_name]
        print(f"Created directory '{full_path}'")
    
    def set_shortcut(self, name: str, filename: str = None):
        """
        Add a shortcut to this folder using the Shortcut manager.

        Parameters
        ----------
        name : str
            The name of the shortcut to add.

        Examples
        --------
        >>> folder = Folder(name="root")
        >>> folder.set_shortcut("my_folder")
        Shortcut 'my_folder' added for path '/root'
        """
        if filename is None:
            self._pn_object.sc.add(name, self.dir())
        else:
            self._pn_object.sc.add(name, self.join(filename))

    def get(self, filename: str):
        """
        Get the full path of a file in the current folder.

        Parameters
        ----------
        filename : str
            The name of the file to get.

        Returns
        -------
        str
            The full path to the file.

        Examples
        --------
        >>> folder = Folder(name="root")
        >>> folder.get("file1")
        '/home/user/root/file1'
        """
        valid_name = self._pn_converter.to_valid_name(filename)
        if valid_name not in self.files:
            print(f"'{filename}' not found in '{self.dir()}'")
            return None
        return self.files[valid_name]
        

    def chdir(self):
        """
        Set this directory as working directory.

        Examples
        --------
        >>> folder.chdir()
        """
        os.chdir(self.dir())
        print(f"Changed working directory to '{self.dir()}'")

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
        if self.dir() not in sys.path:
            if method == 'insert':
                sys.path.insert(index, self.dir())
                print(f"Inserted {self.dir()} at index {index} in system path.")
            elif method == 'append':
                sys.path.append(self.dir())
                print(f"Appended {self.dir()} to system path.")
            else:
                print(f"Invalid method: {method}. Use 'insert' or 'append'.")
        else:
            print(f"{self.dir()} is already in the system path.")

@dataclass
class Shortcut:
    """
    A class to manage shortcuts to specific paths and access them as attributes.

    Methods
    -------
    add(name, path)
        Adds a new shortcut as an attribute.
    remove(name)
        Removes an existing shortcut by name and deletes the attribute.
    get(name)
        Retrieves the path associated with a shortcut.
    ls()
        Lists all shortcuts (attributes).
    to_json(filename)
        Returns all shortcuts as a JSON string and saves it to a file.
    to_dict()
        Returns all shortcuts as a dictionary.
    load_dict(data)
        Loads shortcuts from a dictionary.
    load_json(filename)
        Loads shortcuts from a JSON file.
    """

    def __setattr__(self, name: str, value: str):
        """
        Dynamically add shortcut as an attribute.

        Parameters
        ----------
        name : str
            The name of the shortcut.
        value : str
            The path that the shortcut refers to.
        """
        if name in self.__dict__:
            raise AttributeError(f"Cannot add shortcut '{name}' as it conflicts with an existing attribute.")
        super().__setattr__(name, value)
        print(f"Shortcut '{name}' added for path '{value}'")

    def __getattr__(self, name: str) -> str:
        """
        Retrieve the path of a shortcut.

        Parameters
        ----------
        name : str
            The name of the shortcut.

        Returns
        -------
        str
            The path associated with the shortcut.

        Raises
        ------
        AttributeError
            If the shortcut does not exist.
        """
        if name not in self.__dict__:
            raise AttributeError(f"No shortcut found for '{name}'")
        return self.__dict__[name]

    def __delattr__(self, name: str):
        """
        Remove a shortcut by name.

        Parameters
        ----------
        name : str
            The name of the shortcut to remove.

        Raises
        ------
        AttributeError
            If the shortcut does not exist.
        """
        if name not in self.__dict__:
            raise AttributeError(f"No shortcut found for '{name}'")
        super().__delattr__(name)
        print(f"Shortcut '{name}' removed")

    def add(self, name: str, path: str):
        """
        Add a new shortcut as an attribute.

        Parameters
        ----------
        name : str
            The name of the shortcut.
        path : str
            The path that the shortcut refers to.

        Examples
        --------
        >>> shortcut = Shortcut()
        >>> shortcut.add("my_folder", "/path/to/folder")
        >>> shortcut.my_folder
        '/path/to/folder'
        """
        self.__setattr__(name, path)

    def remove(self, name: str):
        """
        Remove a shortcut by name and delete its attribute.

        Parameters
        ----------
        name : str
            The name of the shortcut to remove.

        Examples
        --------
        >>> shortcut = Shortcut()
        >>> shortcut.add("my_folder", "/path/to/folder")
        >>> shortcut.remove("my_folder")
        >>> hasattr(shortcut, "my_folder")
        False
        """
        self.__delattr__(name)

    def ls(self):
        """
        List all shortcuts and their paths.

        Examples
        --------
        >>> shortcut = Shortcut()
        >>> shortcut.add("my_folder", "/path/to/folder")
        >>> shortcut.ls()
        Shortcuts:
        my_folder -> /path/to/folder
        """
        attributes = {key: value for key, value in self.__dict__.items()}
        if not attributes:
            print("No shortcuts available.")
        else:
            print("Shortcuts:")
            for name, path in attributes.items():
                print(f"{name} -> {path}")
    
    def to_json(self, filename: str) -> str:
        """
        Return all shortcuts as a JSON string and save it to a file.

        Parameters
        ----------
        filename : str
            The name of the file where the JSON string will be saved.

        Returns
        -------
        str
            A JSON string representation of all shortcuts.

        Examples
        --------
        >>> shortcut = Shortcut()
        >>> shortcut.add("my_folder", "/path/to/folder")
        >>> shortcut.to_json("shortcuts.json")
        '{"my_folder": "/path/to/folder"}'
        """
        json_data = json.dumps(self.__dict__, indent=4)  # Converting the dictionary to a pretty-printed JSON string
        with open(filename, 'w') as f:
            f.write(json_data)  # Writing the JSON data to the file
    
        return json_data  # Returning the JSON string as well

    def to_dict(self) -> dict:
        """
        Return all shortcuts as a dictionary.

        Returns
        -------
        dict
            A dictionary representation of all shortcuts.

        Examples
        --------
        >>> shortcut = Shortcut()
        >>> shortcut.add("my_folder", "/path/to/folder")
        >>> shortcut.to_dict()
        {'my_folder': '/path/to/folder'}
        """
        return self.__dict__.copy()

    def load_dict(self, data: dict):
        """
        Load shortcuts from a dictionary.

        Parameters
        ----------
        data : dict
            A dictionary where keys are shortcut names and values are paths.

        Examples
        --------
        >>> shortcut = Shortcut()
        >>> shortcut.load_dict({"project": "/path/to/project", "data": "/path/to/data"})
        """
        for name, path in data.items():
            self.add(name, path)

    def load_json(self, filename: str):
        """
        Load shortcuts from a JSON file.

        Parameters
        ----------
        filename : str
            The name of the file containing the shortcuts in JSON format.

        Examples
        --------
        >>> shortcut = Shortcut()
        >>> shortcut.load_json("shortcuts.json")
        """
        with open(filename, 'r') as f:
            data = json.load(f)  # Load the JSON data into a dictionary
            self.load_dict(data)  # Load the shortcuts using the load_dict method

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
    >>> pm = PathNavigator('/path/to/root')
    >>> pm.mkdir('folder1', 'folder2')     # make a subfolder under the root
    >>> pm.folder1.dir()        # returns the full path to folder1.
    >>> pm.folder1.ls()         # prints the contents (subfolders and files) of folder1.
    >>> pm.folder1.file1        # returns the full path to file1.
    >>> pm.remove('folder1')    # removes a file or subfolder from the folder and deletes it from the filesystem.
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
                valid_folder_name = self._pn_converter.to_valid_name(folder_name)
                new_subfolder = Folder(folder_name, parent_path=current_path, _pn_object=self)
                current_folder.subfolders[valid_folder_name] = new_subfolder
                self._pn_load_nested_directories(entry.path, new_subfolder)
            elif entry.is_file():
                file_name = entry.name #.replace('.', '_').replace(" ", "_")
                valid_filename = self._pn_converter.to_valid_name(file_name)
                current_folder.files[valid_filename] = entry.path
    
    def reload(self):
        """
        Reload the entire folder structure from the root directory.

        Examples
        --------
        >>> pm = PathNavigator('/path/to/root')
        >>> pm.reload()
        """
        self._pn_load_nested_directories(self._pn_root, self)


    
    
