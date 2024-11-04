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
pip install git+https://github.com/philip928lin/path_manager.git
```

## Get start

```python
from pathnavigator import PathNavigator

pn = PathNavigator("root_dir")

# Now you are able to access all subfolders and files under `root_dir`
dir_to_your_subfolder = pn.your_subfolder.get()
path_to_your_file = pn.your_subfolder.get("your_file.csv")  # return the full path to your_file.csv.

# Convert a Path object to a string
path_string = str(dir_to_your_subfolder)

# Prints a visual tree structure of the folder and its contents.
pn.tree() 
pn.your_subfolder.tree()
```

## Features

### Creating Directories
```python
pn = PathNavigator('/path/to/root')
pn.mkdir('folder1')     # make a subfolder under the root.
pn.folder1.mkdir('folder2')     # make a subfolder under folder1.
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

### Directory and File Operations
```python
# Returns the full path to folder1.
pn.folder1.get()       

# Return the full path to file1.
pn.folder1.get("file.csv")  

# Rrints the contents (subfolders and files) of folder1.
pn.folder1.ls()         

# Make the nested directories.
pn.folder1.mkdir("subfolder1", "subsubfolder2")

# Removes a file or subfolder from the folder and deletes it from the filesystem.
pn.folder1.remove('folder2')    

# Combine folder1 directory with "subfolder1/fileX.txt" and return it.
pn.folder1.join("subfolder1", "fileX.txt") 

# Or, you can utilize Path feature to join the paths.
pn.folder1.get() / "subfolder1/fileX.txt"

```

### Shortcuts Management
#### Add shortcuts
```python
# Set a shortcut named "f1" to folder1.
pn.folder1.set_shortcuts("f1")

# Set a shortcut named "x" to the file "x.txt" in folder1.
pn.folder1.set_shortcuts("x", "x.txt")

# Directly add shortcuts in pn.sc
pn.sc.add('f', pn.folder1.get("file"))  
pn.sc.add('f', r"new/path")  
```

#### Retrieve shortcuts
```python
# Retrieve the path of "f1" shortcut
pn.sc.get("f1")  
# Or, access it using "valid" attribute names.
pn.sc.f1    
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