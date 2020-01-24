import os
from ipywidgets import Dropdown, Text, Select, Button, HTML
from ipywidgets import Layout, GridBox, HBox, VBox
from .utils import get_subpaths, get_dir_contents


class FileChooser(VBox):
    """FileChooser class."""

    _LBL_TEMPLATE = '<span style="margin-left:10px; color:{1};">{0}</span>'
    _LBL_NOFILE = 'No file selected'

    def __init__(
            self,
            path=os.getcwd(),
            filename='',
            title='',
            select_desc='Select',
            change_desc='Change',
            show_hidden=False,
            select_default=False,
            **kwargs):
        """Initialize FileChooser object."""
        self._default_path = path.rstrip(os.path.sep)
        self._default_filename = filename
        self._selected_path = None
        self._selected_filename = None
        self._show_hidden = show_hidden
        self._select_desc = select_desc
        self._change_desc = change_desc
        self._callback = None

        # Widgets
        self._pathlist = Dropdown(
            description="",
            layout=Layout(
                width='auto',
                grid_area='pathlist'
            )
        )
        self._filename = Text(
            placeholder='output filename',
            layout=Layout(
                width='auto',
                grid_area='filename'
            )
        )
        self._dircontent = Select(
            rows=8,
            layout=Layout(
                width='auto',
                grid_area='dircontent'
            )
        )
        self._cancel = Button(
            description='Cancel',
            layout=Layout(
                width='auto',
                display='none'
            )
        )
        self._select = Button(
            description=self._select_desc,
            layout=Layout(width='auto')
        )

        self._title = HTML(
            value=title
        )

        if title == '':
            self._title.layout.display = 'none'

        # Widget observe handlers
        self._pathlist.observe(
            self._on_pathlist_select,
            names='value'
        )
        self._dircontent.observe(
            self._on_dircontent_select,
            names='value'
        )
        self._filename.observe(
            self._on_filename_change,
            names='value'
        )
        self._select.on_click(self._on_select_click)
        self._cancel.on_click(self._on_cancel_click)

        # Selected file label
        self._label = HTML(
            value=self._LBL_TEMPLATE.format(
                self._LBL_NOFILE,
                'black'
            ),
            placeholder='',
            description=''
        )

        # Layout
        self._gb = GridBox(
            children=[
                self._pathlist,
                self._filename,
                self._dircontent
            ],
            layout=Layout(
                display='none',
                width='500px',
                grid_gap='0px 0px',
                grid_template_rows='auto auto',
                grid_template_columns='60% 40%',
                grid_template_areas='''
                    'pathlist filename'
                    'dircontent dircontent'
                    '''
            )
        )
        buttonbar = HBox(
            children=[
                self._select,
                self._cancel,
                self._label
            ],
            layout=Layout(width='auto')
        )

        # Call setter to set initial form values
        self._set_form_values(
            self._default_path,
            self._default_filename
        )

        # Use the defaults as the selected values
        if select_default:
            self._apply_selection()

        # Call VBox super class __init__
        super().__init__(
            children=[
                self._title,
                self._gb,
                buttonbar,
            ],
            layout=Layout(width='auto'),
            **kwargs
        )

    def _set_form_values(self, path, filename):
        """Set the form values."""
        # Disable triggers to prevent selecting an entry in the Select
        # box from automatically triggering a new event.
        self._pathlist.unobserve(
            self._on_pathlist_select,
            names='value'
        )
        self._dircontent.unobserve(
            self._on_dircontent_select,
            names='value'
        )
        self._filename.unobserve(
            self._on_filename_change,
            names='value'
        )

        # Set form values
        self._pathlist.options = get_subpaths(path)
        self._pathlist.value = path
        self._filename.value = filename
        self._dircontent.options = get_dir_contents(
            path,
            hidden=self._show_hidden
        )

        # If the value in the filename Text box equals a value in the
        # Select box and the entry is a file then select the entry.
        if ((filename in self._dircontent.options) and
                os.path.isfile(os.path.join(path, filename))):
            self._dircontent.value = filename
        else:
            self._dircontent.value = None

        # Reenable triggers again
        self._pathlist.observe(
            self._on_pathlist_select,
            names='value'
        )
        self._dircontent.observe(
            self._on_dircontent_select,
            names='value'
        )
        self._filename.observe(
            self._on_filename_change,
            names='value'
        )

        # Update the state of the select button
        if self._gb.layout.display is None:
            # Disable the select button if path and filename
            # - equal an existing folder in the current view
            # - equal the already selected values
            check1 = (filename in self._dircontent.options)
            check2 = (os.path.isdir(os.path.join(path, filename)))
            check3 = False

            # Only check selected if selected is set
            if ((self._selected_path is not None) and
                    (self._selected_filename is not None)):
                selected = os.path.join(
                    self._selected_path,
                    self._selected_filename
                )
                check3 = (os.path.join(path, filename) == selected)

            if (check1 and check2) or check3:
                self._select.disabled = True
            else:
                self._select.disabled = False

    def _on_pathlist_select(self, change):
        """Handle selecting a path entry."""
        self._set_form_values(
            change['new'],
            self._filename.value
        )

    def _on_dircontent_select(self, change):
        """Handle selecting a folder entry."""
        new_path = os.path.realpath(
            os.path.join(self._pathlist.value, change['new'])
        )

        # Check if folder or file
        if os.path.isdir(new_path):
            path = new_path
            filename = self._filename.value
        elif os.path.isfile(new_path):
            path = self._pathlist.value
            filename = change['new']

        self._set_form_values(
            path,
            filename
        )

    def _on_filename_change(self, change):
        """Handle filename field changes."""
        self._set_form_values(
            self._pathlist.value,
            change['new']
        )

    def _on_select_click(self, b):
        """Handle select button clicks."""
        if self._gb.layout.display == 'none':
            # If not shown, open the dialog
            self._show_dialog()
        else:
            # If shown, close the dialog and apply the selection
            self._apply_selection()
            # Execute callback function
            if self._callback is not None:
                try:
                    self._callback(self)
                except TypeError:
                    # Support previous behaviour of not passing self
                    self._callback()

    def _show_dialog(self):
        """Show the dialog."""
        # Show dialog and cancel button
        self._gb.layout.display = None
        self._cancel.layout.display = None

        # Show the form with the correct path and filename
        if ((self._selected_path is not None) and
                (self._selected_filename is not None)):
            path = self._selected_path
            filename = self._selected_filename
        else:
            path = self._default_path
            filename = self._default_filename

        self._set_form_values(path, filename)

    def _apply_selection(self):
        """Close the dialog and apply the selection."""
        self._gb.layout.display = 'none'
        self._cancel.layout.display = 'none'
        self._select.description = self._change_desc
        self._selected_path = self._pathlist.value
        self._selected_filename = self._filename.value

        selected = os.path.join(
            self._selected_path,
            self._selected_filename
        )

        if os.path.isfile(selected):
            self._label.value = self._LBL_TEMPLATE.format(
                selected,
                'orange'
            )
        else:
            self._label.value = self._LBL_TEMPLATE.format(
                selected,
                'green'
            )

    def _on_cancel_click(self, b):
        """Handle cancel button clicks."""
        self._gb.layout.display = 'none'
        self._cancel.layout.display = 'none'
        self._select.disabled = False

    def reset(self, path=None, filename=None):
        """Reset the form to the default path and filename."""
        self._selected_path = ''
        self._selected_filename = ''

        self._label.value = self._LBL_TEMPLATE.format(
            self._LBL_NOFILE,
            'black'
        )

        if path is not None:
            self._default_path = path.rstrip(os.path.sep)

        if filename is not None:
            self._default_filename = filename

        self._set_form_values(
            self._default_path,
            self._default_filename
        )

    def refresh(self):
        """Re-render the form."""
        self._set_form_values(
            self._pathlist.value,
            self._filename.value
        )

    @property
    def show_hidden(self):
        """Get current number of rows."""
        return self._show_hidden

    @show_hidden.setter
    def show_hidden(self, hidden):
        """Set number of rows."""
        self._show_hidden = hidden
        self.refresh()

    @property
    def rows(self):
        """Get current number of rows."""
        return self._dircontent.rows

    @rows.setter
    def rows(self, rows):
        """Set number of rows."""
        self._dircontent.rows = rows

    @property
    def title(self):
        """Get the title."""
        return self._title.value

    @title.setter
    def title(self, title):
        """Set the title."""
        self._title.value = title

        if title == '':
            self._title.layout.display = 'none'
        else:
            self._title.layout.display = None

    @property
    def default(self):
        """Get the default value."""
        return os.path.join(
            self._default_path,
            self._default_filename
        )

    @property
    def default_path(self):
        """Get the default_path value."""
        return self._default_path

    @default_path.setter
    def default_path(self, path):
        """Set the default_path."""
        self._default_path = path.rstrip(os.path.sep)
        self._set_form_values(
            self._default_path,
            self._filename.value
        )

    @property
    def default_filename(self):
        """Get the default_filename value."""
        return self._default_filename

    @default_filename.setter
    def default_filename(self, filename):
        """Set the default_filename."""
        self._default_filename = filename
        self._set_form_values(
            self._pathlist.value,
            self._default_filename
        )

    @property
    def selected(self):
        """Get selected value."""
        try:
            return os.path.join(
                self._selected_path,
                self._selected_filename
            )
        except TypeError:
            return None

    @property
    def selected_path(self):
        """Get selected_path value."""
        return self._selected_path

    @property
    def selected_filename(self):
        """Get the selected_filename."""
        return self._selected_filename

    def __repr__(self):
        """Build string representation."""
        str_ = ("FileChooser("
                "path='{0}', "
                "filename='{1}', "
                "show_hidden='{2}')").format(
            self._default_path,
            self._default_filename,
            self._show_hidden
        )
        return str_

    def register_callback(self, callback):
        """Register a callback function."""
        self._callback = callback
