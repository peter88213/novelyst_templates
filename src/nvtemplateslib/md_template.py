"""Provide a class for Markdown story template representation.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvtemplateslib.nvtemplates_globals import *


class MdTemplate:
    """Markdown story template representation.
    
    Public methods:
        read() -- Parse the file and get the instance variables.
        write() -- Write instance variables to the file.

    Public instance variables:
        filePath -- str: path to the file (property with getter and setter). 
    """
    DESCRIPTION = _('Story Template')
    EXTENSION = '.md'

    def __init__(self, filePath, ui):
        """Initialize instance variables.

        Positional arguments:
            filePath -- str: path to the file represented by the File instance.
        """
        self.filePath = filePath
        self._ui = ui

    def read(self):
        """Parse the Markdown file and create parts, chapters, and scenes.
        
        Raise the "Error" exception in case of error. 
        """
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

                #--- Add a Todo scene.
                newTitle = mdLine[5:]
                scId = self._ui.tv.add_scene(title=newTitle, scType=2)
                if scId:
                    newElement = self._ui.novel.scenes[scId]
            elif mdLine.startswith('###'):
                if not parent:
                    continue

                #--- Add a Todo chapter.
                newTitle = mdLine[4:]
                chId = self._ui.tv.add_chapter(title=newTitle, chType=2)
                if chId:
                    newElement = self._ui.novel.chapters[chId]
            elif mdLine.startswith('##'):
                if not parent:
                    continue

                #--- Add a Todo part.
                newTitle = mdLine[3:]
                chId = self._ui.tv.add_part(title=newTitle, chType=2)
                if chId:
                    newElement = self._ui.novel.chapters[chId]
            elif mdLine.startswith('#'):

                #--- Get the parent node for the next new element.
                parent = mdLine[2:]
                try:
                    self._ui.tv.tree.selection_set(parent)
                except:
                    raise Error(f'{_("Wrong heading")}: "{parent}"')
            elif mdLine:
                desc.append(mdLine)

    def write(self):
        """Iterate the project structure and write "Todo" elements to a Markdown file.
        
        Raise the "Error" exception in case of error. 
        """
        mdLines = []
        planningSection = False
        for chId in self._ui.novel.srtChapters:
            if self._ui.novel.chapters[chId].chType != 2:
                continue

            if self._ui.novel.chapters[chId].chLevel == 1:
                # part begins
                if not planningSection:
                    mdLines.append('# pl')
                    planningSection = True
                mdLines.append(f'## {self._ui.novel.chapters[chId].title}')
            else:
                # chapter begins
                if not mdLines:
                    mdLines.append('# nv')
                mdLines.append(f'### {self._ui.novel.chapters[chId].title}')
            desc = self._ui.novel.chapters[chId].desc
            if desc:
                mdLines.append(desc.replace('\n', '\n\n'))
            for scId in self._ui.novel.chapters[chId].srtScenes:
                mdLines.append(f'#### {self._ui.novel.scenes[scId].title}')
                desc = self._ui.novel.scenes[scId].desc
                if desc:
                    mdLines.append(desc.replace('\n', '\n\n'))

        content = '\n\n'.join(mdLines)
        try:
            with open(self.filePath, 'w', encoding='utf-8') as f:
                f.write(content)
        except:
            raise Error(f'{_("Cannot write file")}: "{norm_path(self.filePath)}".')

