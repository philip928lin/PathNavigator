[![PyPI](https://img.shields.io/pypi/v/pathnavigator)](https://pypi.org/project/pathnavigator/)
[![Docs](https://github.com/philip928lin/PathNavigator/actions/workflows/docs.yml/badge.svg)](https://philip928lin.github.io/PathNavigator/)
![Test](https://github.com/philip928lin/PathNavigator/actions/workflows/test.yml/badge.svg)

# PathNavigator

`PathNavigator` is a Python package designed to navigate directories and files efficiently. It provides tools to interact with the filesystem, allowing users to create, delete, and navigate folders and files, while also maintaining an internal representation of the directory structure. Customized shortcuts can be added. The paths are stored as `Path` objects from [`pathlib`](https://docs.python.org/3/library/pathlib.html), which adapt automatically across platforms. 


## Installation

```bash
pip install PathNavigator
```

Install the latest version from GitHub repo:
```bash
pip install git+https://github.com/philip928lin/PathNavigator.git
```

## Get start

```python
from pathnavigator import PathNavigator

pn = PathNavigator("root_dir")

pn.folder1.get()        # returns the full path to folder1 as a Path object.
pn.folder1.get_str()    # returns the full path to folder1 as a string. Same as str(pn.folder1.get()).
pn.folder1.get("file.txt")        # returns the full path to file.txt as a Path object.
pn.folder1.get_str("file.txt")    # returns the full path to file.txt as a string. Same as str(pn.folder1.get("file.txt")).

pn.folder1.set_sc('my_folder')  # set the shortcut to folder1 which can be accessed by pn.sc.my_folder or pn.sc.get("my_folder") or pn.sc.get_str("my_folder").
pn.folder1.set_sc('my_file', 'file.txt')  # set the shortcut to file.txt which can be accessed by pn.sc.my_file or pn.sc.get("my_file") or pn.sc.get_str("my_file").
pn.sc.add('shortcut_name', 'shortcut_path')    # add a customized shortcut independent to pn internal folder structure.

pn.folder1.ls()         # prints the contents (subfolders and files) of folder1.
pn.tree()               # prints the entire nested folder structure.

pn.folder1.chdir()      # change the current directory to folder1.
pn.folder1.add_to_sys_path()    # add folder1 to the system path.

pn.mkdir('folder1', 'folder2')  # make a subfolder under the root. In this case, 'root/folder1/folder2' will be created.
pn.remove('folder1')    # removes a file or subfolder from the folder and deletes it from the filesystem.
```

## Features

### Directory and File Operations
```python
# Returns the full path to folder1.
pn.folder1.get()        # Return a Path object
pn.folder1.get_str()    # Return a string

# Return the full path to file1.
pn.folder1.get("file.csv")      # Return a Path object
pn.folder1.get_str("file.csv")  # Return a string

# Rrints the contents (subfolders and files) of folder1.
pn.folder1.ls()         

# Make the nested directories.
# Directory root/folder1/subfolder1/subsubfolder2 will be created
pn.folder1.mkdir("subfolder1", "subsubfolder2")

# Removes a file or a folder and deletes it from the filesystem including all nested items.
# The following code will delete the directory of root/folder1/folder2
pn.folder1.remove('folder2')    

# Combine folder1 directory with "subfolder1/fileX.txt" and return it.
pn.folder1.join("subfolder1", "fileX.txt") 

# Or, you can utilize Path feature to join the paths.
pn.folder1.get() / "subfolder1/fileX.txt"
```

### Reloading folder structure
```python
# Update the folder structure to fit the latest structure in the file system.
pn.reload() 
```

### System Path Management
```python
# Add the directory to folder1 to sys path.
pn.forlder1.add_to_sys_path()   
```

### Changing Directories
```python
# Change the working directory to folder2.
pn.forlder1.forlder2.chdir()    
```

### Shortcuts Management
#### Add shortcuts
```python
# Set a shortcut named "f1" to folder1.
# Can be accessed by pn.sc.f1 or pn.sc.get("f1") or pn.sc.get_str("f1").
pn.folder1.set_sc("f1")

# Set a shortcut named "x" to the file "x.txt" in folder1.
# Can be accessed by pn.sc.x or pn.sc.get("x") or pn.sc.get_str("x").
pn.folder1.set_sc("x", "x.txt")

# Directly add shortcuts in pn.sc
pn.sc.add('f', pn.folder1.get("file"))  
pn.sc.add('f', r"new/path")  
```

#### Retrieve shortcuts
```python
# Retrieve the path of "f1" shortcut
pn.sc.f1
pn.sc.get("f1")  
pn.sc.get_str("f1") 
```

#### Other shortcut operations
```python
# Print all shortcuts
pn.sc.ls()       

# Remove a shortcut
pn.sc.remove('f')   

# Return a dictionary of shortcuts
pn.sc.to_dict()  

# Output of shortcuts json file
pn.sc.to_json(filename)  

# Load shortcuts from a dictionary
pn.sc.load_dict()  

# Load shortcuts from a json file
pn.sc.load_json(filename)  
```

## API reference
[![Docs](https://github.com/philip928lin/PathNavigator/actions/workflows/docs.yml/badge.svg)](https://philip928lin.github.io/PathNavigator/)