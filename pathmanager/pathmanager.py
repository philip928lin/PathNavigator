import os
from dataclasses import dataclass, field
from typing import Dict
import warnings
import pprint

@dataclass
class PathManager:
    wd: str
    subfolders: Dict[str, str] = field(default_factory=dict)
    files: Dict[str, str] = field(default_factory=dict)
    otherpaths: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        # Change to working directory
        # os.chdir(self.wd)

        # Search for subfolders in the working directory and add them
        for subfolder in os.listdir(self.wd):
            subfolder_path = os.path.join(self.wd, subfolder)
            if os.path.isdir(subfolder_path):
                self.add_subfolder(subfolder)

        # Prepopulate with default files

    def _check_name_eligibility(self, name: str) -> bool:
        """
        Checks if the name is eligible to be used as an attribute name.
        """
        is_eligible = name.isidentifier() and not hasattr(self, name)
        if is_eligible is False:
            raise ValueError(f"{name} has been used/is not a valid attribute name.")

    def _check_path_existence_and_create(self, path: str) -> None:
        """
        Checks if the directory exists and creates it if not.
        """
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"New directory created at: {path}")

    def chdir(self):
        """Change to the working directory."""
        os.chdir(self.wd)
    
    def initiate_project(self, proj_subfolders = [
        "code", "data", "figures", "inputs", "outputs", "models"
        ]):
        """
        Initiates a project by creating the subfolders in the working directory.

        Parameters
        ----------
        proj_subfolders : list
            A list of subfolders to create in the working directory (if not exist).
        """
        # Prepopulate with proj_subfolders
        for subfolder in proj_subfolders:
            self.add_subfolder(subfolder)

    def add_subfolder(self, subfolder: str) -> None:
        """
        Adds a subfolder path to the list of subfolders and sets it as an attribute.
        Ensures the subfolder path is relative to the working directory.

        Parameters
        ----------
        subfolder : str
            The name of the subfolder to add.
        """
        self._check_name_eligibility(subfolder)

        full_path = os.path.join(self.wd, subfolder)
        self._check_path_existence_and_create(full_path)
        self.subfolders[subfolder] = full_path
        setattr(self, subfolder, full_path)

    def remove_subfolder(self, subfolder: str) -> None:
        """
        Removes a subfolder path from the list of subfolders and deletes the attribute.

        Parameters
        ----------
        subfolder : str
            The name of the subfolder to remove.
        """
        if subfolder in self.subfolders:
            del self.subfolders[subfolder]
            if hasattr(self, subfolder):
                delattr(self, subfolder)
        else:
            warnings.warn(f"{subfolder} is not a tracked subfolder.", UserWarning)

    def add_nested_folder(self, parent_subfolder: str, nested_folder: str) -> None:
        """
        Adds a nested folder within a subfolder.

        Parameters
        ----------
        parent_subfolder : str
            The name of the parent subfolder.
        nested_folder : str
            The name of the nested folder to add.
        """
        self._check_name_eligibility(f"{parent_subfolder}_{nested_folder}")

        if parent_subfolder in self.subfolders:
            full_path = os.path.join(self.subfolders[parent_subfolder], nested_folder)
            self._check_path_existence_and_create(full_path)
            setattr(self, f"{parent_subfolder}_{nested_folder}", full_path)
        else:
            raise ValueError(f"{parent_subfolder} is not a tracked subfolder.")

    def remove_nested_folder(self, parent_subfolder: str, nested_folder: str) -> None:
        """
        Removes a nested folder within a subfolder.

        Parameters
        ----------
        parent_subfolder : str
            The name of the parent subfolder.
        nested_folder : str
            The name of the nested folder to remove.
        """
        nested_attr_name = f"{parent_subfolder}_{nested_folder}"
        if hasattr(self, nested_attr_name):
            full_path = getattr(self, nested_attr_name)
            if os.path.exists(full_path):
                os.rmdir(full_path)  # This only works if the directory is empty
            delattr(self, nested_attr_name)
        else:
            warnings.warn(
                f"{nested_attr_name} is not a tracked nested folder.", UserWarning
            )

    def add_file(self, file_name: str, subfolder: str = None, name: str = None) -> None:
        """
        Adds a file path to the list of files. If subfolder is specified, the file path is relative to that subfolder.
        Raises an error if the file does not exist.

        Parameters
        ----------
        file_name : str
            The name of the file to add.
        subfolder : str, optional
            The name of the subfolder to add the file to.
        """
        if subfolder:
            if subfolder in self.subfolders:
                full_path = os.path.join(self.subfolders[subfolder], file_name)
            else:
                raise ValueError(f"{subfolder} is not a tracked subfolder.")
        else:
            full_path = os.path.join(self.wd, file_name)

        if os.path.isfile(full_path):
            if name:
                self._check_name_eligibility(name)
                self.files[name] = full_path
                setattr(self, name, full_path)
            else:
                file_name_without_extension = os.path.splitext(file_name)[0]
                self._check_name_eligibility(file_name_without_extension)
                self.files[file_name_without_extension] = full_path
                setattr(self, file_name_without_extension, full_path)
        else:
            raise FileNotFoundError(f"{full_path} does not exist.")

    def remove_file(self, file_name: str) -> None:
        """
        Removes a file path from the list of files and deletes the attribute.

        Parameters
        ----------
        file_name : str
            The name of the file to remove.
        """
        if file_name in self.files:
            del self.files[file_name]
            if hasattr(self, file_name):
                delattr(self, file_name)
        else:
            warnings.warn(f"{file_name} is not a tracked file.", UserWarning)

    def add_other_path(self, name: str, path: str) -> None:
        """
        Adds a folder or file path to the dictionary of otherpaths and sets it as an
        attribute.

        Parameters
        ----------
        name : str
            The name of the attribute to add.
        path : str
            The path to add.
        """
        self._check_name_eligibility(name)
        is_dir = os.path.isdir(path)
        is_file = os.path.isfile(path)

        if is_dir:
            self.otherpaths[name] = path
            setattr(self, name, path)
        elif is_file:
            self.otherpaths[name] = path
            setattr(self, name, path)
        elif not is_dir and not is_file:
            if "." in path:  # Assume . means files
                raise FileNotFoundError(f"{path} does not exist.")
            else:
                try:
                    self._check_path_existence_and_create(path)
                    self.otherpaths[name] = path
                    setattr(self, name, path)
                except:
                    raise FileNotFoundError(f"{path} does not exist.")
        else:
            raise FileNotFoundError(f"{path} does not exist.")

    def remove_other_path(self, name: str) -> None:
        """
        Removes a folder or file path from the dictionary of otherpaths and deletes the
        attribute.

        Parameters
        ----------
        name : str
            The name of the attribute to remove.
        path : str
            The path to remove.
        """
        if name in self.otherpaths:
            del self.otherpaths[name]
            if hasattr(self, name):
                delattr(self, name)
        else:
            warnings.warn(f"{name} is not a tracked name of otherpaths.", UserWarning)

    def get_subfolders(self) -> Dict[str, str]:
        """
        Returns the dictionary of subfolder paths.
        """
        return self.subfolders

    def get_files(self) -> Dict[str, str]:
        """
        Returns the dictionary of file paths.
        """
        return self.files

    def get_otherpaths(self) -> Dict[str, str]:
        """
        Returns the dictionary of file paths.
        """
        return self.otherpaths

    def list(self):
        """Print the attributes in a pretty format."""
        pp = pprint.PrettyPrinter(indent=4)
        print("Working Directory (wd):")
        pp.pprint(self.wd)
        print("\nSubfolders:")
        pp.pprint(self.subfolders)
        print("\nFiles:")
        pp.pprint(self.files)
        print("\nOther Paths:")
        pp.pprint(self.otherpaths)