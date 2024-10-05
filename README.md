# PathManager

`PathManager` is a Python package designed to manage directories and files efficiently. It provides tools to interact with the filesystem, allowing users to create, delete, and navigate folders and files, while also maintaining an internal representation of the directory structure.


## Installation

```bash
pip install git+https://github.com/philip928lin/path_manager.git
```

## Get start

```python
from pathmanager import PathManager

pm = PathManager("root_dir")

# Now you are able to access all subfolders and files under `root_dir`
dir_to_your_subfolder = pm.your_subfolder.dir()  
path_to_your_file = pm.your_subfolder.your_file_txt # "." will be replaced by "_"
```

## Other features
```python
pm = PathManager('/path/to/root')
pm.mkdir('folder1', 'folder2')  # make a subfolder under the root
pm.forlder1.add_to_sys_path()   # add dir to folder1 to sys path.
pm.folder1.dir()        # returns the full path to folder1.
pm.folder1.ls()         # prints the contents (subfolders and files) of folder1.
pm.folder1.file1        # returns the full path to file1.
pm.remove('folder1')    # removes a file or subfolder from the folder and deletes it from the filesystem.
```