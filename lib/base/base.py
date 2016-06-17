#!/usr/bin/python
# -*-  coding: utf-8 -*-

##
# Current source: https://github.com/open-security/vulnpwn/
##

from lib.base import framework
from lib.utils import randoms
import importlib
import sys
import os


class Base(framework.Framework):
    def __init__(self, verbose=False):
        self.app_name = 'vulnpwn'
        self.module_prompt_fmt = '%s \033[33m%s\033[m > '
        self.origin_prompt_fmt = '%s > '
        self.prompt = self.origin_prompt_fmt % self.app_name

        framework.Framework.__init__(self, verbose)

        self.app_path = self.dirpath(self.dirpath(self.dirpath(__file__)))

        self.data_path = os.path.join(self.app_path, 'data', '')
        self.logos_path = os.path.join(self.app_path, 'data', 'logos', '')
        self.mods_path = os.path.join(self.app_path, 'modules', '')

        self.modules = self.index_modules(self.mods_path)
        self.modules_dirs = [_ for _ in os.listdir(self.mods_path)
                             if not _.startswith("__")]

        self.current_module = None

        self.show_commands = [_ for _ in dir(self) if _.startswith('show_')]

        # self.import_modules()
        ('base.base' in self.__module__) and self.do_banner()

    def index_modules(self, mods_dir):
        """ Return list of all exploits modules """

        modules = []
        for root, dirs, files in os.walk(mods_dir):
            _, package, root = root.rpartition(mods_dir.replace('/', os.sep))
            root = root.replace(os.sep, '.')
            files = filter(
                 lambda x: not x.startswith("__") and x.endswith('.py'), files)
            modules.extend(
                map(lambda x: '.'.join((root, os.path.splitext(x)[0])), files))

        return modules

    def import_module(self, path):
        """Import a module. Because this function is meant for use by the Python
        interpreter and not for general use it is better to use
        importlib.import_module() to programmatically import a module

        syntax: importlib.import_module('abc.XXX.def.YYY')
        """
        # http://stackoverflow.com/questions/301134/dynamic-module-import-in-python
        # http://stackoverflow.com/questions/21213355/python-difference-between-import-and-import-as
        # http://stackoverflow.com/questions/211100/pythons-import-doesnt-work-as-expected

        try:
            module = importlib.import_module(path)
            return module
        except (ImportError, AttributeError, KeyError) as err:
            print(err)

    def import_modules(self):
        """Load all valid modules"""
        modules = map(lambda x: "".join(['modules.', x]), self.modules)
        map(self.import_module, modules)

    def do_back(self, line):
        """Move back from the current context"""
        self.prompt = self.origin_prompt_fmt % self.app_name

    def do_banner(self):
        """Display an awesome framework banner"""
        colors = [framework.Colors.R, framework.Colors.G,
                  framework.Colors.O, framework.Colors.B]

        logo_files = self.dirwalk(self.logos_path)
        path = randoms.rand_item_from_iters(logo_files)

        if path:
            print(randoms.rand_item_from_iters(colors))
            print(self.readfile(path))
            print(framework.Colors.N)

            # print module total information
            print(randoms.rand_item_from_iters(colors))
            info = ('       =[ %s v1.00                      ]=\n'
                    '+ -- --=[ get more about security !          ]=-- -- +\n'
                    % (self.app_name))
            print(info)
            print(framework.Colors.N)

    def do_edit(self, line):
        """Edit the current module with $VISUAL or $EDITOR"""
        self.editfile(sys.argv[0])

    def do_use(self, line):
        """Load framework module"""
        key, value, paris = self.parseline(line)

        if (not key):
            self.help_load()
            return False

        self.prompt = self.module_prompt_fmt % (self.app_name, line)

        module_path = line.replace(os.path.sep, '.')
        module_path = ''.join(['modules.', module_path])
        self.current_module = self.import_module(module_path)

    def do_show(self, line):
        """Show available options / modules"""
        key, value, pairs = self.parseline(line)

        if (not key):
            self.help_show()
            return False

        method = 'show_%s' % key
        if method in self.show_commands and hasattr(self, method):
            func = getattr(self, method)
            func()

    def show_modules(self):
        """Show available modules"""
        modules = map(lambda x: x.replace('.', os.path.sep), self.modules)
        map(self.output, modules)

    def complete_show(self, line, text, *ignored):
        """Tab complete show"""
        if line:
            line = "show_%s" % line
            methods = self.available_show_completion(line)
        else:
            methods = self.show_commands

        return map(lambda x: x.replace('show_', ''), methods)

    def complete_use(self, line, text, *ignored):
        """Tab complete show"""
        if line:
            return self.available_modules_completion(line)
        else:
            return self.modules_dirs

    def available_show_completion(self, text):
        """match all possible show commands"""
        return filter(lambda x: x.startswith(text), self.show_commands)

    def available_modules_completion(self, text):
        """match all possible modules"""
        modules = map(lambda x: x.replace('.', os.path.sep), self.modules)
        return filter(lambda x: x.startswith(text), modules)

    def help_edit(self):
        self.output('')
        self.output('  Usage :  edit <module>')
        self.output('  Desp  :  %s' % getattr(self, 'do_edit').__doc__)
        self.output('  Demo  :  edit')
        self.output('')

    def help_show(self):
        self.output('')
        self.output('  Usage :  show | show <options | modules>')
        self.output('  Desp  :  %s' % getattr(self, 'do_show').__doc__)
        self.output('  Demo  :  show options')
        self.output('')

    def help_use(self):
        self.output('')
        self.output('  Usage :  use <module>')
        self.output('  Desp  :  %s' % getattr(self, 'do_load').__doc__)
        self.output('  Demo  :  use auxiliary/scanner/http/http_title')
        self.output('')
