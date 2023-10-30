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
        filePath: str -- path to the file (property with getter and setter). 
    """
    DESCRIPTION = _('Story Template')
    EXTENSION = '.md'
    ARC_MARKER = '-'

    def __init__(self, filePath, ui):
        """Initialize instance variables.

        Positional arguments:
            filePath: str -- path to the file represented by the File instance.
        """
        self.filePath = filePath
        self._ui = ui

    def read(self):
        """Parse the Markdown file and create parts, chapters, and scenes.
        
        Raise the "Error" exception in case of error. 
        """
        try:
            with open(self.filePath, 'r', encoding='utf-8') as f:
                mdLines = f.readlines()
        except(FileNotFoundError):
            raise Error(f'{_("File not found")}: "{norm_path(self.filePath)}".')
        except:
            raise Error(f'{_("Cannot read file")}: "{norm_path(self.filePath)}".')

        if mdLines[0].startswith('# nv'):
            self.read_novelyst4_structure(mdLines)
        else:
            self.read_novelyst5_structure(mdLines)

    def read_novelyst4_structure(self, mdLines):
        chId = self._ui.tv.add_chapter(selection=CH_ROOT, title=_('Stages'), chLevel=2, chType=3)
        scId = chId
        arcSection = False
        newElement = None
        desc = []
        for mdLine in mdLines:
            mdLine = mdLine.strip()
            if mdLine.startswith('#'):
                if newElement is not None:
                    newElement.desc = ''.join(desc).strip().replace('  ', ' ')
                    desc = []
                    newElement = None
                if mdLine.startswith('####'):
                    if arcSection:
                        # Add a second-level stage.
                        newTitle = mdLine[5:]
                        scId = self._ui.tv.add_stage(selection=scId, title=newTitle, stageLevel=2)
                        if scId:
                            newElement = self._ui.novel.scenes[scId]
                elif mdLine.startswith('###'):
                    if not arcSection:
                        # Add a first-level stage.
                        newTitle = mdLine[4:]
                        scId = self._ui.tv.add_stage(selection=scId, title=newTitle, stageLevel=1)
                        if scId:
                            newElement = self._ui.novel.scenes[scId]
                elif mdLine.strip() == '# pl':
                    arcSection = True
            elif mdLine:
                desc.append(f'{mdLine} ')
            else:
                desc.append('\n')
        try:
            newElement.desc = ''.join(desc).strip().replace('  ', ' ')
        except AttributeError:
            pass

    def read_novelyst5_structure(self, mdLines):
        if self._ui.novel.chapters:
            self.list_stages(mdLines)
        else:
            self.create_chapter_structure(mdLines)

    def create_chapter_structure(self, mdLines):
        i = 0
        chId = CH_ROOT
        addChapter = True
        newElement = None
        desc = []
        for mdLine in mdLines:
            mdLine = mdLine.strip()
            if mdLine.startswith('#'):
                if newElement is not None:
                    newElement.desc = ''.join(desc).strip().replace('  ', ' ')
                    desc = []
                    newElement = None
                if mdLine.startswith('## '):
                    # Add a 2nd level stage.
                    if addChapter:
                        i += 1
                        chId = self._ui.tv.add_chapter(selection=chId, title=f"{_('Chapter')} {i}", chLevel=2, chType=0)
                        scId = chId
                    newTitle = mdLine[3:].strip()
                    scId = self._ui.tv.add_stage(selection=scId, title=newTitle, stageLevel=2)
                    newElement = self._ui.novel.scenes[scId]
                    scId = self._ui.tv.add_scene(selection=scId, title=_('New Scene'), scType=0, status=1)
                    addChapter = True
                elif mdLine.startswith('# '):
                    # Add a ist level stage.
                    i += 1
                    chId = self._ui.tv.add_chapter(selection=chId, title=f"{_('Chapter')} {i}", chLevel=2, chType=0)
                    newTitle = mdLine[2:].strip()
                    scId = self._ui.tv.add_stage(selection=chId, title=newTitle, stageLevel=1)
                    newElement = self._ui.novel.scenes[scId]
                    addChapter = False
                else:
                    scId = None
            elif mdLine:
                desc.append(f'{mdLine} ')
            else:
                desc.append('\n')
        newElement.desc = ''.join(desc).strip().replace('  ', ' ')

    def list_stages(self, mdLines):
        chId = self._ui.tv.add_chapter(selection=CH_ROOT, title=_('Stages'), chLevel=2, chType=3)
        scId = chId
        newElement = None
        desc = []
        for mdLine in mdLines:
            mdLine = mdLine.strip()
            if mdLine.startswith('#'):
                if newElement is not None:
                    newElement.desc = ''.join(desc).strip().replace('  ', ' ')
                    desc = []
                    newElement = None
                if mdLine.startswith('## '):
                    # Add a 2nd level stage.
                    newTitle = mdLine[3:].strip()
                    scId = self._ui.tv.add_stage(selection=scId, title=newTitle, stageLevel=2)
                elif mdLine.startswith('# '):
                    # Add a 1st level stage.
                    newTitle = mdLine[2:].strip()
                    scId = self._ui.tv.add_stage(selection=scId, title=newTitle, stageLevel=1)
                else:
                    scId = None
                if scId:
                    newElement = self._ui.novel.scenes[scId]
            elif mdLine:
                desc.append(f'{mdLine} ')
            else:
                desc.append('\n')
        newElement.desc = ''.join(desc).strip().replace('  ', ' ')

    def write(self):
        """Iterate the project structure and write the new elements to a Markdown file.
        
        Raise the "Error" exception in case of error. 
        """
        mdLines = []
        for chId in self._ui.novel.tree.get_children(CH_ROOT):
            for scId in self._ui.novel.tree.get_children(chId):
                if self._ui.novel.scenes[scId].stageLevel == 1:
                    mdLines.append(f'# {self._ui.novel.scenes[scId].title}')
                    desc = self._ui.novel.scenes[scId].desc
                    if desc:
                        mdLines.append(desc.replace('\n', '\n\n'))
                elif self._ui.novel.scenes[scId].stageLevel == 2:
                    mdLines.append(f'## {self._ui.novel.scenes[scId].title}')
                    desc = self._ui.novel.scenes[scId].desc
                    if desc:
                        mdLines.append(desc.replace('\n', '\n\n'))

        content = '\n\n'.join(mdLines)
        try:
            with open(self.filePath, 'w', encoding='utf-8') as f:
                f.write(content)
        except:
            raise Error(f'{_("Cannot write file")}: "{norm_path(self.filePath)}".')

