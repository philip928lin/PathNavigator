import re
import keyword
from dataclasses import dataclass, field

@dataclass
class AttributeNameConverter:
    """
    A class to convert original names to valid attribute names and store the mapping.

    Methods
    -------
    to_valid_name(name)
        Convert the original name to a valid attribute name.
    get(name)
        Get the valid attribute name for the given original name.
    """
    _pn_org_to_valid_name: dict = field(default_factory=dict)
    _pn_valid_name_to_org: dict = field(default_factory=dict)

    def to_valid_name(self, name: str) -> str:
        """Convert the original name to a valid attribute name."""
        if self._pn_is_valid_attribute_name(name) is False:
            valid_name = self._pn_convert_to_valid_attribute_name(name)
            #print(f"Convert '{name}' to a valid attribute name, '{valid_name}'.")
            return valid_name
        else:
            return name

    def get(self, name: str) -> str:
        """
        Get the valid attribute name for the given original name.
        
        Parameters
        ----------
        name : str
            The original name to get the valid attribute name for.
        """
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
        """
        Check if a given attribute name is valid.
        
        Parameters
        ----------
        name : str
            The attribute name to check.
        invalid_list : list, optional
            A list of invalid attribute names. Default is a list of reserved names.
        """
        if name.startswith('_pn_'):
            raise ValueError(f"Strings starting with '_pn_' are reserved in PathNavigator. Please modify '{name}' to eligible naming.")
        return name.isidentifier() and not keyword.iskeyword(name) and not name in invalid_list

    def _pn_convert_to_valid_attribute_name(self, name: str) -> str:
        """
        Convert ineligible attribute name to a valid one.
        
        Parameters
        ----------
        name : str
            The original name to convert.
        """
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
        """
        Check if the original name needs to use the name mapping.
        
        Parameters
        ----------
        name : str
            The original name to check.
        """
        return name in self._pn_valid_name_to_org
    