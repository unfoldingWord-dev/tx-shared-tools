# -*- coding: utf8 -*-
#
#  Copyright (c) 2016 unfoldingWord
#  http://creativecommons.org/licenses/MIT/
#  See LICENSE file for details.
#
#  Contributors:
#  Richard Mahn <richard_mahn@wycliffeassociates.org>

from __future__ import unicode_literals

import sys


def str_to_class(str):
    """
    Gets a class from a string.
    :param str|unicode str: The string of the class name
    """
    return reduce(getattr, str.split("."), sys.modules[__name__])
