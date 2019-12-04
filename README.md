# ipyfilechooser

A simple Python file chooser widget for use in Jupyter/IPython in conjunction with ipywidgets. The selected path and file are available via `.selected_path` and `.selected_filename` respectvely or as a single combined filepath via `.selected`. The dialog can be reset to its default path and filename by using `.reset()`. 

When a typed filename matches an existing file entry in the current folder the entry will be highlighted. If a typed filename matches a folder entry in the current view the selection button is disabled ensure the user is aware of the match. To select a folder simply leave the filename field empty.

To emphasize the risk of overwriting existing files, the selected filepath is displayed in green if the file does not exist and orange if it does. 

[![Downloads](https://pepy.tech/badge/ipyfilechooser)](https://pepy.tech/project/ipyfilechooser)

## Usage

```
from ipyfilechooser import FileChooser

# Create and display a FileChooser widget
fc = FileChooser('/Users/crahan/FC demo')
display(fc)

# Print the selected path, filename, or both
print(fc.selected_path)
print(fc.selected_filename)
print(fc.selected)

# Change defaults and reset the dialog
fc.default_path = '/Users/crahan/'
fc.default_filename = 'output.txt'
fc.reset()

# Shorthand reset
fc.reset(path='/Users/crahan/', filename='output.txt')

# Change hidden files
fc.show_hidden = True

# Change the title (use '' to hide)
fc.title = '<b>FileChooser title</b>'
```

## Functions and variables

```
fc.reset()
fc.refresh()
fc.register_callback(function_name)
fc.show_hidden
fc.rows
fc.title
fc.default
fc.default_path
fc.default_filename
fc.selected
fc.selected_path
fc.selected_filename
```

## Screenshots

### Closed vs open dialog

![Screenshot 1](https://github.com/crahan/ipyfilechooser/raw/master/screenshots/FileChooser_screenshot_1.png)

![Screenshot 2](https://github.com/crahan/ipyfilechooser/raw/master/screenshots/FileChooser_screenshot_2.png)

### Existing vs new file selection

![Screenshot 3](https://github.com/crahan/ipyfilechooser/raw/master/screenshots/FileChooser_screenshot_3.png)

![Screenshot 4](https://github.com/crahan/ipyfilechooser/raw/master/screenshots/FileChooser_screenshot_4.png)

### Quick navigation dropdown

![Screenshot 5](https://github.com/crahan/ipyfilechooser/raw/master/screenshots/FileChooser_screenshot_5.png)


## Release notes

### 0.3.1

- Option to register a callback function (`register_callback(function_name)`)

### 0.3.0

- Ability to select a folder
- Support for Windows drive letters
- Option to use the defaults as the selected value

### 0.2.0

- First public release
