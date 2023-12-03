"""Provide global variables and functions.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/noveltree_templates
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
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
           'ROOT_PREFIX',
           'ARC_PREFIX',
           'ARC_POINT_PREFIX',
           'CHAPTER_PREFIX',
           'CH_ROOT',
           'AC_ROOT',
           ]
ROOT_PREFIX = 'rt'
CHAPTER_PREFIX = 'ch'
ARC_PREFIX = 'ac'
ARC_POINT_PREFIX = 'ap'
CH_ROOT = f'{ROOT_PREFIX}{CHAPTER_PREFIX}'
AC_ROOT = f'{ROOT_PREFIX}{ARC_PREFIX}'


class Error(Exception):
    """Base class for exceptions."""
    pass


# Initialize localization.
LOCALE_PATH = f'{os.path.dirname(sys.argv[0])}/locale/'
try:
    CURRENT_LANGUAGE = locale.getlocale()[0][:2]
except:
    # Fallback for old Windows versions.
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

