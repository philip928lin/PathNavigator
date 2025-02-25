# V0.5.1
- Replaced `load_nested_dirs()` in the `PathNavigator` class with `scan()` in the `Folder` class.
- Added include and exclude regex patterns to the `scan()` method in the `Folder` class.
- Consolidated `listdirs()` and `listfiles()` into a single `list()` method in the `Folder` class.
- Enhanced the `get()` method to accept variable arguments (`*args`).