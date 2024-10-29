![Docs](https://github.com/philip928lin/PathNavigator/actions/workflows/docs.yml/badge.svg)
![Test](https://github.com/philip928lin/PathNavigator/actions/workflows/test.yml/badge.svg)

# PathNavigator

`PathNavigator` is a Python package designed to navigate directories and files efficiently. It provides tools to interact with the filesystem, allowing users to create, delete, and navigate folders and files, while also maintaining an internal representation of the directory structure. Customized shortcuts can be added.


## Installation

```bash
pip install PathNavigator
```

Install the latest version from GitHub repo
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
pn.tree() # print out folder structure.
```

Note that all the paths stored/retured are represented as `Path` object from [`pathlib`](https://docs.python.org/3/library/pathlib.html).

## Features

### Creating Directories
```python
pn = PathNavigator('/path/to/root')
pn.mkdir('folder1')     # make a subfolder under the root.
pn.folder1.mkdir('folder2')     # make a subfolder under folder1.
```

### System Path Management
```python
pn.forlder1.add_to_sys_path()   # add dir to folder1 to sys path.
```

### Changing Directories
```python
pn.forlder1.forlder2.chdir()    # change the working directory to folder2.
```

### Directory and File Operations
```python
pn.folder1.get()        # returns the full path to folder1.
pn.folder1.get("file.csv")  # return the full path to file1.
pn.folder1.file1        # returns the full path to file1 (if file1 is a valid attribute name).
pn.folder1.ls()         # prints the contents (subfolders and files) of folder1.
pn.folder1.remove('folder2')    # removes a file or subfolder from the folder and deletes it from the filesystem.
pn.folder1.join("subfolder1", "fileX.txt") # combine folder1 directory with "subfolder1/fileX.txt" and return it.
```

### Shortcuts Management
```python
pn.folder1.set_shortcuts("f1")  # set a shortcut named "f1" to folder1.
pn.sc.f1    # retrieve the path of "f1" shortcut
pn.sc.get("f1")  # retrieve the path of "f1" shortcut

pn.sc.add('f', pn.folder1.file)    # add shortcut, "f", to the file.
pn.f               # retrieve the path of a specific shortcut (i.e., "f")
pn.sc.get("f")  # retrieve the path of "f" shortcut
pn.sc.ls()       # print all shortcuts
pn.sc.remove('f')   # remove a shortcut
pn.sc.to_dict()  # return a dictionary of shortcuts
pn.sc.to_json(filename)  # output of shortcuts json file
pn.sc.load_dict()  # load shortcuts from a dictionary
pn.sc.load_json(filename)  # load shortcuts from a json file
```

## API reference
[philip928lin.github.io/PathNavigator/](https://philip928lin.github.io/PathNavigator/)
