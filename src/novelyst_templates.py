"""A "Story Templates" plugin for novelyst.

Version @release

Adds a 'Add Story Templates' entry to the 'Tools' menu to open a window
with a combobox that lists all available themes. 
The selected theme will be persistently applied.  

Requires Python 3.6+
Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst_templates
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import tkinter as tk
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
    NOVELYST_API = '4.12'
    DESCRIPTION = 'A "Story Templates" manager'
    URL = 'https://peter88213.github.io/novelyst_templates'

    def install(self, ui):
        """Add a submenu to the 'Tools' menu.
        
        Positional arguments:
            ui -- reference to the NovelystTk instance of the application.
        """
        self._ui = ui

        # Create menu entry
        self._templatesMenu = tk.Menu(self._ui.toolsMenu, tearoff=0)
        self._templatesMenu.add_command(label=_('Load'), command=self._load_template)
        self._templatesMenu.add_command(label=_('Save'), command=self._save_template)

        # Create menu entry
        self._ui.toolsMenu.add_cascade(label=APPLICATION, menu=self._templatesMenu)
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')
        self._fileTypes = [(MdTemplate.DESCRIPTION, MdTemplate.EXTENSION)]

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        self._ui.toolsMenu.entryconfig(APPLICATION, state='normal')

    def _load_template(self):
        """Create a structure of "Todo" chapters and scenes from a Markdown file."""
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            templateDir = f'{homeDir}/.pywriter/novelyst/templates'
        except:
            templateDir = '.'
        fileName = filedialog.askopenfilename(filetypes=self._fileTypes,
                                              defaultextension=self._fileTypes[0][1],
                                              initialdir=templateDir)
        try:
            templates = MdTemplate(fileName, self._ui)
            templates.read()
        except Error as ex:
            messagebox.showerror(_('Template loading aborted'), str(ex))

    def _save_template(self):
        """Save a structure of "Todo" chapters and scenes to a Markdown file."""
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            templateDir = f'{homeDir}/.pywriter/novelyst/templates'
        except:
            templateDir = '.'
        fileName = filedialog.asksaveasfilename(filetypes=self._fileTypes,
                                              defaultextension=self._fileTypes[0][1],
                                              initialdir=templateDir)
        if not fileName:
            return

        try:
            templates = MdTemplate(fileName, self._ui)
            templates.write()
        except Error as ex:
            messagebox.showerror(_('Cannot save template'), str(ex))

        self._ui.set_info_how(_('Template saved.'))
