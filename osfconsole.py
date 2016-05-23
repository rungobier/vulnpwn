#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# Current source: https://github.com/open-security/Open-Security-Framework/
##


import sys


sys.dont_write_bytecode = True

from lib.base import base


try:
    fw = base.Base()
    fw.cmdloop()
except KeyboardInterrupt:
    fw.output('')
    fw.output('exit.')
