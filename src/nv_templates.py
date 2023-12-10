"""A "Story Templates" plugin for noveltree.

Version @release

Adds a 'Add Story Templates' entry to the 'Tools' menu to open a window
with a combobox that lists all available themes. 
The selected theme will be persistently applied.  

Requires Python 3.6+
Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/nv_templates
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
import os
import tkinter as tk
import webbrowser
from tkinter import messagebox
from tkinter import filedialog
from pathlib import Path
from nvtemplateslib.nvtemplates_globals import *
from nvtemplateslib.md_template import MdTemplate


class Plugin():
    """A 'Story Templates' plugin class.
    
    Public methods:
        disable_menu() -- disable menu entries when no project is open.
        enable_menu() -- enable menu entries when a project is open.    
    """
    VERSION = '@release'
    NOVELYST_API = '0.1'
    DESCRIPTION = 'A "Story Templates" manager'
    URL = 'https://peter88213.github.io/nv_templates'
    _HELP_URL = 'https://peter88213.github.io/nv_templates/usage'

    def install(self, ui):
        """Add a submenu to the 'Tools' menu.
        
        Positional arguments:
            ui -- reference to the NovelystTk instance of the application.
        """
        self._ui = ui
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            self._templateDir = f'{homeDir}/.noveltree/templates'
        except:
            self._templateDir = '.'

        # Create "Story Templates" submenu.
        self._templatesMenu = tk.Menu(self._ui.toolsMenu, tearoff=0)
        self._templatesMenu.add_command(label=_('Load'), command=self._load_template)
        self._templatesMenu.add_command(label=_('Save'), command=self._save_template)
        self._templatesMenu.add_command(label=_('Open folder'), command=self._open_folder)

        # Create Tools menu entry.
        self._ui.toolsMenu.add_cascade(label=APPLICATION, menu=self._templatesMenu)
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')
        self._fileTypes = [(MdTemplate.DESCRIPTION, MdTemplate.EXTENSION)]

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(label=_('Templates plugin Online help'), command=lambda: webbrowser.open(self._HELP_URL))

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        self._ui.toolsMenu.entryconfig(APPLICATION, state='normal')

    def _load_template(self):
        """Create a structure of "Todo" chapters and scenes from a Markdown file."""
        fileName = filedialog.askopenfilename(filetypes=self._fileTypes,
                                              defaultextension=self._fileTypes[0][1],
                                              initialdir=self._templateDir)
        if fileName:
            try:
                templates = MdTemplate(fileName, self._ui)
                templates.read()
            except Error as ex:
                messagebox.showerror(_('Template loading aborted'), str(ex))

    def _save_template(self):
        """Save a structure of "Todo" chapters and scenes to a Markdown file."""
        fileName = filedialog.asksaveasfilename(filetypes=self._fileTypes,
                                              defaultextension=self._fileTypes[0][1],
                                              initialdir=self._templateDir)
        if not fileName:
            return

        try:
            templates = MdTemplate(fileName, self._ui)
            templates.write()
        except Error as ex:
            messagebox.showerror(_('Cannot save template'), str(ex))

        self._ui.set_info_how(_('Template saved.'))

    def _open_folder(self):
        """Open the templates folder with the OS file manager."""
        try:
            os.startfile(norm_path(self._templateDir))
            # Windows
        except:
            try:
                os.system('xdg-open "%s"' % norm_path(self._templateDir))
                # Linux
            except:
                try:
                    os.system('open "%s"' % norm_path(self._templateDir))
                    # Mac
                except:
                    pass
