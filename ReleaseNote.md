# v0.5.4
- Add `user = os.getlogin()` to the package
- Add `os_name = platform.system()` to detect the operating system

# v0.5.3
- Generalize `add_all_files` to `add_all`
- Debug `shortcut.get()` and  `att_name_convertor.py`

# v0.5.2
- Add `display` arg to `PathNavigator` to avoid massive output when running in parallel.

# v0.5.1
- Replaced `load_nested_dirs()` in the `PathNavigator` class with `scan()` in the `Folder` class.
- Added include and exclude regex patterns to the `scan()` method in the `Folder` class.
- Consolidated `listdirs()` and `listfiles()` into a single `list()` method in the `Folder` class.
- Enhanced the `get()` method to accept variable arguments (`*args`).
