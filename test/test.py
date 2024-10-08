import os
import shutil
from pathnavigator.pathnavigator import Folder, PathNavigator  # Replace with your actual module name

def test_folder_class():
    print("Testing Folder class...")

    # Create a temporary root directory
    temp_root = "temp_root"
    if os.path.exists(temp_root):
        shutil.rmtree(temp_root)
    os.mkdir(temp_root)

    # Create the root folder object
    root_folder = Folder(name="temp_root")

    # Test mkdir
    root_folder.mkdir("subfolder1")
    assert "subfolder1" in root_folder.subfolders, "Subfolder creation failed."
    print("mkdir() passed.")

    # Test __getattr__
    assert root_folder.subfolder1.name == "subfolder1", "__getattr__ method failed."
    print("__getattr__() passed.")

    # Create another subfolder and test
    root_folder.mkdir("subfolder1", "nested_subfolder")
    assert "nested_subfolder" in root_folder.subfolder1.subfolders, "Nested subfolder creation failed."
    print("Nested mkdir() passed.")

    # Test ls
    print("ls() test output:")
    root_folder.ls()  # Expecting the created subfolders to be printed
    print("ls() passed.")

    # Test file creation (manually for now)
    test_file_path = os.path.join(temp_root, "test_file.txt")
    with open(test_file_path, "w") as f:
        f.write("Test file content.")
    root_folder.files["test_file"] = test_file_path

    assert "test_file" in root_folder.files, "File addition failed."
    print("File addition passed.")

    # Test remove (file)
    root_folder.remove("test_file")
    assert not os.path.exists(test_file_path), "File deletion failed."
    print("File remove() passed.")

    # Test remove (folder)
    root_folder.subfolder1.remove("nested_subfolder")
    assert "nested_subfolder" not in root_folder.subfolder1.subfolders, "Subfolder deletion failed."
    print("Subfolder remove() passed.")

    # Cleanup
    shutil.rmtree(temp_root)
    print("Folder tests completed successfully.\n")


def test_path_navigator():
    print("Testing PathNavigator class...")

    # Create a temporary root directory with some structure
    temp_root = "temp_root"
    if os.path.exists(temp_root):
        shutil.rmtree(temp_root)
    os.mkdir(temp_root)
    
    os.makedirs(os.path.join(temp_root, "subfolder1/nested_subfolder"), exist_ok=True)
    test_file_path = os.path.join(temp_root, "subfolder1", "test_file.txt")
    with open(test_file_path, "w") as f:
        f.write("Test file content.")

    # Initialize PathNavigator
    manager = PathNavigator(temp_root)

    # Test if root was loaded correctly
    assert "subfolder1" in manager.subfolders, "Root directory load failed."
    print("Root directory loaded successfully.")

    # Test nested subfolder access
    assert "nested_subfolder" in manager.subfolder1.subfolders, "Nested subfolder load failed."
    print("Nested subfolder access passed.")

    # Test file access
    assert "test_file_txt" in manager.subfolder1.files, "File load failed."
    print("File access passed.")

    # Test reload
    manager.reload()
    assert "subfolder1" in manager.subfolders, "Reload failed."
    print("Reload passed.")

    # Cleanup
    shutil.rmtree(temp_root)
    print("PathNavigator tests completed successfully.\n")


if __name__ == "__main__":
    # Test Folder class functionalities
    test_folder_class()

    # Test PathNavigator class functionalities
    test_path_navigator()
