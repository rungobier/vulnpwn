#!/usr/bin/python2
# -*- coding: utf-8 -*-

##
# Current source: https://github.com/open-security/vulnpwn/
##

from lib.base import base
from lib.core import item


class Module(base.Base):
    """Module of framework"""

    __info__ = {
        'name': '',
        'description': '',
        'license': '',
        'disclosureDate': '',
        'author': [],
        'references': [],
        'options': {
            # 'key': [default_value, description]
        }
    }

    def __init__(self):
        base.Base.__init__(self, verbose=False)
        self.prompt_mod_fmt = '%s (\033[33m%s\033[m) > '
        self.prompt_mod = self.__module__.replace('.', self.path_sep)
        self.prompt_mod = self.prompt_mod.replace(
            'modules%s' % self.path_sep, '')
        self.prompt = self.prompt_mod_fmt % (self.app_name, self.prompt_mod)

        self.check_module_info()
        self.options = item.Items()

        # self.register_option(self, key, value, default, description):
        for option in self.__info__['options'].items():
            (key, [default_value, desc]) = option
            self.register_option(key, default_value, desc)

    # ======================
    #  OPTIONS COMMANDS
    # ======================

    def check_module_info(self):
        if not self.__info__.get('name', None):
            self.error("Please set module 'name'")

        if not self.__info__.get('description', None):
            self.error("Please set module 'description'")

        if not self.__info__.get('license', None):
            self.error("Please set module 'license'")

        if not self.__info__.get('disclosureDate', None):
            self.error("Please set module 'disclosureDate'")

        if not self.__info__.get('author', None):
            self.error("Please set module 'author'")

        if not self.__info__.get('references', None):
            self.error("Please set module 'references'")

        if not self.__info__.get('options', None):
            self.error("Please set module 'options'")

    def register_option(self, key, default_value, description):
        """register option item to global options"""
        key = self.getUnicode(key)

        self.options[key] = item.Items()
        self.options[key]['value'] = self.getUnicode(default_value)
        self.options[key]['description'] = self.getUnicode(description)

        return self.options

    def max_len(self, values):
        """Show options information with a pretty format"""
        return len(max(values, key=len))

    def show_options(self):
        """Show current options"""
        menu_title = ('Option', 'Current Setting', 'Description')

        keys = self.options.keys()
        values = [item['value'] for item in self.options.values()]
        descriptions = [item['description'] for item in self.options.values()]

        # calc max column length
        if len(keys) > 0:
            key_maxlen = max(self.max_len(keys), len(menu_title[0]))
        else:
            key_maxlen = len(menu_title[0])

        if len(values) > 0:
            val_maxlen = max(self.max_len(values), len(menu_title[1]))
        else:
            val_maxlen = len(menu_title[1])

        if len(descriptions) > 0:
            des_maxlen = max(self.max_len(descriptions), len(menu_title[2]))
        else:
            des_maxlen = len(menu_title[2])

        menu_fmt = "    %%-%ds  %%-%ds  %%-%ds" % (
            key_maxlen, val_maxlen, des_maxlen)

        self.output('')
        # menu title
        self.output(menu_fmt % menu_title)

        # menu separator
        menu_sep = ('-' * key_maxlen, '-' * val_maxlen, '-' * des_maxlen)
        self.output(menu_fmt % menu_sep)

        # menu options
        if len(keys) == len(values) == len(descriptions):
            menu_opts = zip(keys, values, descriptions)
            for menu_opt in menu_opts:
                self.output(menu_fmt % menu_opt)

        self.output('')

    def do_run(self, *args, **kwargs):
        """run module main function"""
        self.main(*args, **kwargs)

    def do_set(self, line):
        """Set key equal to value"""
        key, value, pairs = self.parseline(line)

        if (not key) or (not value):
            self.help_set()
            return False

        if key not in self.options:
            self.error('Please choose a valid option key')
            return False

        self.register_option(key, value, '')
        self.output("SET => %s = (%s) " % (key, value))
        self.options[key]['value'] = value

    def do_unset(self, line):
        """Unset the option"""
        if (not line):
            self.help_unset()
            return False

        if line in self.options:
            self.options[line]['value'] = ''

    def help_set(self):
        self.output('')
        self.output('  Usage :  set <key> <value>')
        self.output('  Desp  :  %s' % getattr(self, 'do_set').__doc__)
        self.output('  Demo  :  set threads 1')
        self.output('')

    def help_unset(self):
        self.output('')
        self.output('  Usage :  unset <key>')
        self.output('  Desp  :  %s' % getattr(self, 'do_unset').__doc__)
        self.output('  Demo  :  unset keyname')
        self.output('')

    def main(self, *args, **kwargs):
        pass
