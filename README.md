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
from pathmanager import PathNavigator

pn = PathNavigator("root_dir")

# Now you are able to access all subfolders and files under `root_dir`
dir_to_your_subfolder = pn.your_subfolder.dir()  
path_to_your_file = pn.your_subfolder.your_file_txt # "." will be replaced by "_"
```

## Other features
```python
pn = PathNavigator('/path/to/root')
pn.mkdir('folder1')     # make a subfolder under the root.
pn.folder1.mkdir('folder2')     # make a subfolder under folder1.
pn.forlder1.add_to_sys_path()   # add dir to folder1 to sys path.
pn.forlder1.forlder2.chdir()    # change the working directory to folder2.
pn.folder1.dir()        # returns the full path to folder1.
pn.folder1.ls()         # prints the contents (subfolders and files) of folder1.
pn.folder1.file1        # returns the full path to file1.
pn.folder1.remove('folder2')    # removes a file or subfolder from the folder and deletes it from the filesystem.

pn.shortcuts.add('config', pn.folder1.file)    # add shortcut to, e.g., config file.
pn.config               # retrieve the path of a specific shortcut
pn.shortcuts.ls()       # print all shortcuts
pn.shortcuts.remove('config')   # remove a shortcut
pn.shortcuts.to_dict()  # return a dictionary of shortcuts
pn.shortcuts.to_json(filename)  # output of shortcuts json file
pn.shortcuts.load_dict()  # load shortcuts from a dictionary
pn.shortcuts.load_json(filename)  # load shortcuts from a json file
```