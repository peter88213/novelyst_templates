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
import sys
import gettext
import locale

__all__ = ['Error',
           '_',
           'norm_path',
           'LOCALE_PATH',
           'CURRENT_LANGUAGE',
           'APPLICATION',
           'PLUGIN',
           ]


class Error(Exception):
    pass


LOCALE_PATH = f'{os.path.dirname(sys.argv[0])}/locale/'
try:
    CURRENT_LANGUAGE = locale.getlocale()[0][:2]
except:
    CURRENT_LANGUAGE = locale.getdefaultlocale()[0][:2]
try:
    t = gettext.translation('novelyst_templates', LOCALE_PATH, languages=[CURRENT_LANGUAGE])
    _ = t.gettext
except:

    def _(message):
        return message

APPLICATION = _('Story Templates')
PLUGIN = f'{APPLICATION} plugin @release'


def norm_path(path):
    if path is None:
        path = ''
    return os.path.normpath(path)



class MdTemplate:
    DESCRIPTION = _('Story Template')
    EXTENSION = '.md'

    def __init__(self, filePath, ui):
        self.filePath = filePath
        self._ui = ui

    def read(self):
        try:
            with open(self.filePath, 'r', encoding='utf-8') as f:
                content = f.read()
        except(FileNotFoundError):
            raise Error(f'{_("File not found")}: "{norm_path(self.filePath)}".')
        except:
            raise Error(f'{_("Cannot read file")}: "{norm_path(self.filePath)}".')

        mdLines = content.split('\n')
        parent = None
        newElement = None
        desc = []
        for mdLine in mdLines:
            if mdLine.startswith('#'):
                if newElement is not None:
                    newElement.desc = '\n'.join(desc)
                    desc = []
                    newElement = None
            if mdLine.startswith('####'):
                if not parent:
                    continue

                newTitle = mdLine[5:]
                scId = self._ui.tv.add_scene(title=newTitle, scType=2)
                if scId:
                    newElement = self._ui.novel.scenes[scId]
            elif mdLine.startswith('###'):
                if not parent:
                    continue

                newTitle = mdLine[4:]
                chId = self._ui.tv.add_chapter(title=newTitle, chType=2)
                if chId:
                    newElement = self._ui.novel.chapters[chId]
            elif mdLine.startswith('##'):
                if not parent:
                    continue

                newTitle = mdLine[3:]
                chId = self._ui.tv.add_part(title=newTitle, chType=2)
                if chId:
                    newElement = self._ui.novel.chapters[chId]
            elif mdLine.startswith('#'):

                parent = mdLine[2:]
                try:
                    self._ui.tv.tree.selection_set(parent)
                except:
                    raise Error(f'{_("Wrong heading")}: "{parent}"')
            elif mdLine:
                desc.append(mdLine)

    def write(self):
        raise Error(f'{self.filePath} Write method is not implemented.')



class Plugin():
    """A 'Story Templates' plugin class.
    
    Public methods:
        disable_menu() -- disable menu entries when no project is open.
        enable_menu() -- enable menu entries when a project is open.    
    """
    VERSION = '@release'
    NOVELYST_API = '4.12'
    DESCRIPTION = 'Creates a story arc framework from a markdown template'
    URL = 'https://peter88213.github.io/novelyst_templates'

    def install(self, ui):
        """Add a submenu to the 'Tools' menu.
        
        Positional arguments:
            ui -- reference to the NovelystTk instance of the application.
        """
        self._ui = ui

        self._templatesMenu = tk.Menu(self._ui.toolsMenu, tearoff=0)
        self._templatesMenu.add_command(label=_('Load'), command=self._load_template)
        self._templatesMenu.add_command(label=_('Save'), command=self._save_template)

        self._ui.toolsMenu.add_cascade(label=APPLICATION, menu=self._templatesMenu)
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')
        self._fileTypes = [(MdTemplate.DESCRIPTION, MdTemplate.EXTENSION)]

    def disable_menu(self):
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')

    def enable_menu(self):
        self._ui.toolsMenu.entryconfig(APPLICATION, state='normal')

    def _load_template(self):
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
