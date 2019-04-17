from ipywidgets import Dropdown, Text, Select, Button, HTML
from ipywidgets import Layout, GridBox, HBox, VBox
from .utils import update_path, get_subpaths, get_dir_contents
import os


class FileChooser(VBox):

    _LBL_TEMPLATE = '<span style="margin-left:10px; color:{1};">{0}</span>'
    _LBL_NOFILE = 'No file selected'

    def __init__(
            self,
            path=os.getcwd(),
            filename='',
            show_hidden=False,
            **kwargs):

        self._default_path = path.rstrip(os.path.sep)
        self._default_filename = filename
        self._selected_path = ''
        self._selected_filename = ''
        self._show_hidden = show_hidden

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
            description='Select',
            layout=Layout(width='auto')
        )

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

        # Call VBox super class __init__
        super().__init__(
            children=[
                self._gb,
                buttonbar,
            ],
            layout=Layout(width='auto'),
            **kwargs
        )

    def _set_form_values(self, path, filename):
        '''Set the form values'''

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

        # Set the state of the select Button
        if self._gb.layout.display is None:
            selected = os.path.join(
                self._selected_path,
                self._selected_filename
            )

            # filename value is empty or equals the selected value
            if (filename == '') or (os.path.join(path, filename) == selected):
                self._select.disabled = True
            else:
                self._select.disabled = False

    def _on_pathlist_select(self, change):
        '''Handler for when a new path is selected'''
        self._set_form_values(
            change['new'],
            self._filename.value
        )

    def _on_dircontent_select(self, change):
        '''Handler for when a folder entry is selected'''
        new_path = update_path(
            self._pathlist.value,
            change['new']
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
        '''Handler for when the filename field changes'''
        self._set_form_values(
            self._pathlist.value,
            change['new']
        )

    def _on_select_click(self, b):
        '''Handler for when the select button is clicked'''
        if self._gb.layout.display is 'none':
            self._gb.layout.display = None
            self._cancel.layout.display = None

            # Show the form with the correct path and filename
            if self._selected_path and self._selected_filename:
                path = self._selected_path
                filename = self._selected_filename
            else:
                path = self._default_path
                filename = self._default_filename

            self._set_form_values(path, filename)

        else:
            self._gb.layout.display = 'none'
            self._cancel.layout.display = 'none'
            self._select.description = 'Change'
            self._selected_path = self._pathlist.value
            self._selected_filename = self._filename.value
            # self._default_path = self._selected_path
            # self._default_filename = self._selected_filename

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
        '''Handler for when the cancel button is clicked'''
        self._gb.layout.display = 'none'
        self._cancel.layout.display = 'none'
        self._select.disabled = False

    def reset(self, path=None, filename=None):
        '''Reset the form to the default path and filename'''
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
        '''Re-render the form'''
        self._set_form_values(
            self._pathlist.value,
            self._filename.value
        )

    @property
    def show_hidden(self):
        '''Get current number of rows'''
        return self._show_hidden

    @show_hidden.setter
    def show_hidden(self, hidden):
        '''Set number of rows'''
        self._show_hidden = hidden
        self.refresh()

    @property
    def rows(self):
        '''Get current number of rows'''
        return self._dircontent.rows

    @rows.setter
    def rows(self, rows):
        '''Set number of rows'''
        self._dircontent.rows = rows

    @property
    def default(self):
        '''Get the default value'''
        return os.path.join(
            self._default_path,
            self._default_filename
        )

    @property
    def default_path(self):
        '''Get the default_path value'''
        return self._default_path

    @default_path.setter
    def default_path(self, path):
        '''Set the default_path'''
        self._default_path = path.rstrip(os.path.sep)
        self._default = os.path.join(
            self._default_path,
            self._filename.value
        )
        self._set_form_values(
            self._default_path,
            self._filename.value
        )

    @property
    def default_filename(self):
        '''Get the default_filename value'''
        return self._default_filename

    @default_filename.setter
    def default_filename(self, filename):
        '''Set the default_filename'''
        self._default_filename = filename
        self._default = os.path.join(
            self._pathlist.value,
            self._default_filename
        )
        self._set_form_values(
            self._pathlist.value,
            self._default_filename
        )

    @property
    def selected(self):
        '''Get selected value'''
        return os.path.join(
            self._selected_path,
            self._selected_filename
        )

    @property
    def selected_path(self):
        '''Get selected_path value'''
        return self._selected_path

    @property
    def selected_filename(self):
        '''Get the selected_filename'''
        return self._selected_filename

    def __repr__(self):
        str_ = ("FileChooser("
                "path='{0}', "
                "filename='{1}', "
                "show_hidden='{2}')").format(
            self._default_path,
            self._default_filename,
            self._show_hidden
        )
        return str_
