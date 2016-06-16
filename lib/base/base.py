#!/usr/bin/python
# -*-  coding: utf-8 -*-

##
# Current source: https://github.com/open-security/vulnpwn/
##

from lib.base import framework
from lib.utils import randoms
from lib.core import item
import threadpool
import sys
import imp
import os


class Base(framework.Framework):
    def __init__(self, verbose=False):
        self.prompt = 'vulnpwn > '
        self.prompt_fmt = '%s (\033[33m%s\033[m) > '

        self.options = item.Items()
        self.mod_info = item.Items()

        framework.Framework.__init__(self, verbose)

        self.app_name = 'vulnpwn'
        self.app_path = self.dirpath(self.dirpath(self.dirpath(__file__)))

        self.data_path = os.path.join(self.app_path, 'data', '')
        self.logos_path = os.path.join(self.app_path, 'data', 'logos', '')
        self.mods_path = os.path.join(self.app_path, 'modules', '')

        self.count_auxiliary = 0
        self.count_exploit = 0
        self.count_payload = 0

        self.loaded_modules = []
        # self.modules = self.index_modules(self.mods_path)
        self.modules_dirs = [_ for _ in os.listdir(self.mods_path)
                             if not _.startswith("__")]

        self.show_commands = [_ for _ in dir(self) if _.startswith('show_')]

        self.import_modules()
        ('base.base' in self.__module__) and self.show_banner()

    # ======================
    #  OPTIONS COMMANDS
    # ======================

    def register_option(self, key, value, default, description):
        """register option item to global options"""
        key = self.getUnicode(key)
        self.options[key] = item.Items()
        if value:
            self.options[key]['value'] = self.getUnicode(value)
        else:
            self.options[key]['value'] = self.getUnicode(default)
        self.options[key]['description'] = self.getUnicode(description)

        return self.options

    # ======================
    #  FRAMEWORK MODULES
    # ======================

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

    def register_module(self, name, dispname, loadpath, mod_obj):
        """register module item to global modules"""
        name = self.getUnicode(name)
        self.mod_info[name] = item.Items()
        if mod_obj:
            self.mod_info[name]['dispname'] = dispname
            self.mod_info[name]['loadpath'] = loadpath
            self.mod_info[name]['modobj'] = mod_obj

    def handle_loadmod_exception(self, func, *args, **kwargs):
        """handle module load exception"""
        try:
            return func(*args, **kwargs)
        except ImportError:
            return None

    def import_module(self, filename):
        """Load a single framwork module"""
        # dname = self.dirpath(filename)
        fname = self.filename(filename)

        if filename.endswith('.py'):
            if 'modules/auxiliary/' in filename:
                self.count_auxiliary += 1
            elif 'modules/exploits/' in filename:
                self.count_exploit += 1
            elif 'modules/payloads/' in filename:
                self.count_payload += 1

            mod_loadpath = filename.replace(self.mods_path, '')
            mod_loadpath = mod_dispname = mod_loadpath.replace('.py', '')

            if mod_loadpath not in self.loaded_modules:
                self.loaded_modules.append(mod_loadpath)

            mod_loadpath = mod_loadpath.replace('/', '_')
            mod_name = fname.replace('.py', '')
            fp = open(filename) if self.is_exists(filename) else None

            if isinstance(fp, file):
                self.handle_loadmod_exception(
                    imp.load_source, mod_loadpath, filename, fp)

                if mod_name not in self.mod_info:
                    self.debug("Load Module => %s" % mod_dispname)
                    __import__(mod_loadpath)

                    # init plugin module class
                    mod_obj = sys.modules[mod_loadpath]
                    mod_obj = mod_obj.Module if hasattr(
                        mod_obj, 'Module') else None
                    self.register_module(
                        mod_name, mod_dispname, filename, mod_obj)

        return self.mod_info

    def import_modules(self):
        """Load framework modules"""
        mods = [mod for mod in self.dirwalk(self.mods_path)
                if ('__init__.py' not in mod) and mod.endswith('.py')]
        map(self.import_module, mods)

    def find_module(self, dispname):
        """find module fullpath with dispname"""
        for key in self.mod_info.keys():
            mod = self.mod_info[key]
            if ('dispname' in mod) and (mod['dispname'] == dispname):
                return mod

        return None

    # ======================
    #  FRAMEWORK THREADS
    # ======================

    def threads_exception(self, request, exc_info):
        """handle per thread exceptions"""
        pass

    def threads_task(self, *args, **kwargs):
        """define per thread tasks"""
        pass

    def threads_task_result(self, request, data):
        """handle per thread result"""
        self.output(request)
        # self.output(data)

    def threads(self, args_kwds=[((None,), {})]):
        """multithreads for tasks"""
        pool = threadpool.ThreadPool(self.options['THREADS'])
        reqs = threadpool.makeRequests(self.threads_task, args_kwds,
                                       self.threads_task_result,
                                       self.threads_exception)
        [pool.putRequest(req) for req in reqs]

        while True:
            try:
                pool.poll()
            except KeyboardInterrupt:
                break
            except threadpool.NoResultsPending:
                break

        if pool.dismissedWorkers:
            pool.joinAllDismissedWorkers()

    # ======================
    #  FRAMEWORK COMMANDS
    # ======================

    def do_edit(self, line):
        """Edit current module"""
        self.editfile(sys.argv[0])

    def do_use(self, line):
        """Load framework module"""
        key, value, paris = self.parseline(line)

        if (not key):
            self.help_load()
            return False

        mod = self.find_module(line)

        loadpath = mod['loadpath'] if mod else ''
        modobj = mod['modobj'] if mod else None

        # self.output("[+] Load Module => %s" % loadpath)
        self.import_module(loadpath)

        if hasattr(modobj, 'cmdloop'):
            plugin = modobj()
            plugin.prompt = self.prompt_fmt % (self.app_name, mod['dispname'])
            plugin.cmdloop()

    #  **** SET METHODS ****

    def do_set(self, line):
        """Set key equal to value"""
        key, value, pairs = self.parseline(line)

        if (not key) or (not value):
            self.help_set()
            return False

        if key not in self.options:
            self.register_option(key, value, None, '')

        self.output("SET => %s = (%s) " % (key, value))
        self.options[key]['value'] = value

    #  **** UNSET METHODS ****

    def do_unset(self, line):
        """Unset the option"""
        if (not line):
            self.help_unset()
            return False

        if line in self.options:
            self.options[line]['value'] = ''

    #  **** SHOW METHODS ****

    def max_len(self, values):
        """Show options information with a pretty format"""
        return len(max(values, key=len))

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

    def show_modules(self):
        """Show available modules"""
        self.output('')
        for key in self.mod_info.keys():
            # mod_name = key
            # mod_loadpath = self.mod_info[key]['loadpath']
            if 'dispname' in self.mod_info[key]:
                mod_dispname = self.mod_info[key]['dispname']
                self.output("    %s" % mod_dispname)
        self.output('')

    def show_banner(self):
        """Show banner"""
        colors = [framework.Colors.R, framework.Colors.G,
                  framework.Colors.O, framework.Colors.B]

        logo_files = self.dirwalk(self.logos_path)
        path = randoms.rand_item_from_iters(logo_files)

        if path:
            # print logo
            print(randoms.rand_item_from_iters(colors))
            print(self.readfile(path))
            print(framework.Colors.N)

            # print module total information
            print(randoms.rand_item_from_iters(colors))
            info = ('       =[ %s v1.00                      ]=\n'
                    '+ -- --=[ %04d auxiliary                     ]=-- -- +\n'
                    '+ -- --=[ %04d exploits                      ]=-- -- +\n'
                    '+ -- --=[ %04d payloads                      ]=-- -- +\n'
                    '+ -- --=[ get more about security !          ]=-- -- +\n'
                    % (self.app_name, self.count_auxiliary,
                       self.count_exploit, self.count_payload))
            print(info)
            print(framework.Colors.N)

    #  **** COMPLETE METHODS ****

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
        return filter(lambda x: x.startswith(text), self.loaded_modules)

    # ======================
    #  FRAMEWORK COMMANDS
    # ======================
    def help_edit(self):
        self.output('')
        self.output('  Usage :  edit <module>')
        self.output('  Desp  :  %s' % getattr(self, 'do_edit').__doc__)
        self.output('  Demo  :  edit')
        self.output('')

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


if __name__ == "__main__":
    base = Base()
    base.cmdloop()
