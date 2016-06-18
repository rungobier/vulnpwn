#!/usr/bin/python2
# -*- coding: utf-8 -*-

##
# Current source: https://github.com/open-security/vulnpwn/
##

from lib.base import base


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
        self.options = self.__info__.get('options')

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

    def get_option_value(self, key):
        value = None
        if key in self.options:
            value = self.options.get(key)[0]
        return value

    def show_options(self):
        """Show current options"""
        menu_title = ('Name', 'Current Setting', 'Description')

        keys = self.options.keys()
        values = [_[0] for _ in self.options.values()]
        descriptions = [_[1] for _ in self.options.values()]

        key_maxlen = max(len(max(map(self.getUnicode, keys), key=len)),
                         len(menu_title[0]))
        val_maxlen = max(len(max(map(self.getUnicode, values), key=len)),
                         len(menu_title[1]))
        des_maxlen = max(len(max(map(self.getUnicode, descriptions), key=len)),
                         len(menu_title[2]))

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

    def do_info(self, *args, **kwargs):
        """Displays information about one or more modules"""
        self.output("")
        self.output("%12s : %s" % ('Name', self.__info__.get('name')))
        self.output("%12s : %s" % ('Module', self.__module__))
        self.output("%12s : %s" % ('Licnese', self.__info__.get('license')))
        self.output("%12s : %s" % ('Disclosed',
                    self.__info__.get('disclosureDate')))
        self.output("")

        authors = self.__info__.get('author')
        if len(authors) > 0:
            self.output("Provided by:")
            for _ in authors:
                self.output("  %s" % _)

        if hasattr(self.options, 'keys') and self.options.keys():
            self.output("")
            self.output("Basic options:")
            self.show_options()

        self.output("")
        self.output("Description:")
        desc = self.__info__.get('description')
        desc_lines = desc.splitlines()
        if len(desc_lines) > 0:
            for _ in desc_lines:
                self.output("  %s" % _.strip())

        self.output("")
        self.output("References:")
        refers = self.__info__.get('references')
        if len(refers) > 0:
            for _ in refers:
                self.output("  %s" % _)
        self.output("")

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

        self.output("%s => %s" % (key, value))
        _, description = self.options.get(key)
        self.options[key] = [value, description]

    def do_unset(self, line):
        """Unset the option"""
        if (not line):
            self.help_unset()
            return False

        if line in self.options:
            value, description = self.options.get(line)
            value = None
            self.options[line] = [value, description]

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
