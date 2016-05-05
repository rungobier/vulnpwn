#!/usr/bin/python2
# -*- coding: utf-8 -*-

##
# Current source: https://github.com/open-security/Open-Security-Framework/
##

from lib.core import base


class Module(base.Base):
    """Module of framework"""

    meta = {
        'name': '',
        'author': '',
        'description': '',
        'comments': '',
        'references': [],
        'license': '',
        'options': {
            # 'key': [value, default, description]
        }
    }

    def __init__(self):
        base.Base.__init__(self, verbose=False)

        # self.register_option(self, key, value, default, description):
        for option in self.meta['options'].items():
            (key, [value, default_value, desc]) = option
            self.register_option(key, value, default_value, desc)

    def show_options(self):
        base.Base.show_options(self)

    def do_run(self, *args, **kwargs):
        """run module main function"""
        self.main(*args, **kwargs)

    def main(self, *args, **kwargs):
        pass
