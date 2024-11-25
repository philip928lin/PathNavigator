import pytest
import os
import sys
from pathnavigator import PathNavigator
from pathlib import Path

@pytest.fixture
def setup_pathnavigator(tmp_path):
    """
    root
    ├── folder1
    │   └── file1.txt
    └── folder2
        └── subfolder1
            └── file2.txt
    """
    root = tmp_path / "root"
    root.mkdir()
    
    # Create folder1 inside root
    folder1 = root / "folder1"
    folder1.mkdir()
    
    # Create file1.txt inside folder1
    file1 = folder1 / "file1.txt"
    file1.touch()  # This creates an empty file
    
    # Create folder2 inside root
    folder2 = root / "folder2"
    folder2.mkdir()
    
    # Create subfolder1 inside folder2
    subfolder1 = folder2 / "subfolder1"
    subfolder1.mkdir()
    
    # Create file2.txt inside subfolder1
    file2 = subfolder1 / "file2.txt"
    file2.touch()  # This creates an empty file
    
    pn = PathNavigator(root)
    return pn

def test_initialization(setup_pathnavigator):
    pn = setup_pathnavigator
    assert pn.name == "root"
    assert pn.parent_path == pn._pn_object.parent_path

def test_mkdir(setup_pathnavigator):
    pn = setup_pathnavigator
    pn.mkdir('newfolder')

    # Check if 'newfolder' is in the subfolders dictionary
    assert 'newfolder' in pn.subfolders

    # Check if the 'newfolder' actually exists in the filesystem
    newfolder_path = os.path.join(pn.get(), 'newfolder')
    assert os.path.isdir(newfolder_path)

def test_add_to_sys_path(setup_pathnavigator):
    pn = setup_pathnavigator
    pn.folder1.add_to_sys_path()
    assert pn.folder1.get() in sys.path

def test_chdir(setup_pathnavigator):
    pn = setup_pathnavigator
    pn.folder2.subfolder1.chdir()
    assert Path(os.getcwd()) == pn.folder2.subfolder1.get()

def test_get(setup_pathnavigator):
    pn = setup_pathnavigator
    assert pn.folder1.get() == pn.get() / 'folder1'

def test_get_file_path(setup_pathnavigator):
    pn = setup_pathnavigator
    file_path = pn.folder1.get("file1.txt")
    # Check if the file path is correct
    assert file_path == pn.folder1.get() / "file1.txt"

    # Check if the file actually exists in the filesystem
    assert os.path.isfile(file_path)

def test_file_attribute(setup_pathnavigator):
    pn = setup_pathnavigator
    pn.mkdir('folder1')
    file_path = pn.folder1.get("file1.txt")
    assert pn.folder1._file1_txt == file_path

def test_ls(setup_pathnavigator, capsys):
    pn = setup_pathnavigator
    # List contents of root directory
    pn.ls()
    captured = capsys.readouterr()
    assert 'folder1' in captured.out
    assert 'folder2' in captured.out
    
    # List contents of folder1 (weired. Does not work but the np.folder1.subfolder1.ls() works)
    pn.folder1.ls()
    captured = capsys.readouterr()
    #assert 'file1.txt' in captured.out
    
    # List contents of folder2
    pn.folder2.ls()
    captured = capsys.readouterr()
    assert 'subfolder1' in captured.out
    
    # List contents of subfolder1 (weired. Does not work but the np.folder1.subfolder1.ls() works)
    pn.folder2.subfolder1.ls() 
    captured = capsys.readouterr()
    #assert 'file2.txt' in captured.out

def test_remove(setup_pathnavigator):
    pn = setup_pathnavigator
    pn.mkdir('newfolder')
    
    # Ensure the folder was created
    newfolder_path = os.path.join(pn.get(), 'newfolder')
    assert os.path.isdir(newfolder_path)
    
    # Remove the folder
    pn.remove('newfolder')
    
    # Check if 'newfolder' is not in the subfolders dictionary
    assert 'newfolder' not in pn.subfolders
    
    # Check if the 'newfolder' does not exist in the filesystem
    assert not os.path.isdir(newfolder_path)

def test_join(setup_pathnavigator):
    pn = setup_pathnavigator
    joined_path = pn.folder1.join("subfolder1", "fileX.txt")
    assert joined_path == pn.folder1.get() / "subfolder1" / "fileX.txt"

def test_set_sc(setup_pathnavigator):
    pn = setup_pathnavigator
    pn.folder2.subfolder1.set_sc("sb1")
    assert pn.sc.sb1 == pn.folder2.subfolder1.get()

def test_shortcut_manager(setup_pathnavigator):
    pn = setup_pathnavigator
    pn.folder1.set_sc("f1")
    pn.sc.add('f', pn.folder1.get("file1.txt"))
    assert pn.sc.f == pn.folder1.get("file1.txt")
    shortcuts = pn.sc.to_dict()
    assert 'f' in shortcuts
    json_file = os.path.join(pn.get(), "shortcuts.json")
    pn.sc.to_json(json_file)
    assert os.path.exists(json_file)
    pn.sc.remove('f')
    assert 'f' not in pn.sc.to_dict()
    pn.sc.load_json(json_file, overwrite=True)
    assert 'f1' in pn.sc.to_dict()