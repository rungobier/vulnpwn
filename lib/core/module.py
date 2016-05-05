#!/usr/bin/python2
# -*- coding: utf-8 -*-

##
# Current source: https://github.com/open-security/Open-Security-Framework/
##

from lib.core import base


class Module(base.Base):
    """Module of framework"""

    Name = ''
    Description = ''
    Author = ''
    References = ''
    License = ''

    def __init__(self):
        base.Base.__init__(self, verbose=False)

    def show_options(self):
        rjust_length = 18
        self.output('')
        self.output("  Name: %s".rjust(rjust_length) % self.Name)
        self.output("  Description: %s".rjust(rjust_length) % self.Description)
        self.output("  Author: %s".rjust(rjust_length) % self.Author)
        self.output("  References: %s".rjust(rjust_length) % self.References)
        base.Base.show_options(self)

    def do_run(self, *args, **kwargs):
        """run module main function"""
        self.main(*args, **kwargs)

    def main(self, *args, **kwargs):
        pass
