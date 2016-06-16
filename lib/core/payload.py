#!/usr/bin/python
# -*-  coding: utf-8 -*-

##
# Current source: https://github.com/open-security/vulnpwn/
##

from lib.base import module


class Payload(module.Module):
    def __init__(self):
        module.Module.__init__(self)
        self.shellcode = ''

    def generate_shellcode(self):
        pass

    def do_generate(self, line):
        '''generate a payload shellcode'''
        self.generate_shellcode()

    def help_generate():
        self.output('')
        self.output('  Usage :  generate')
        self.output('  Desp  :  %s' % getattr(self, 'do_generate').__doc__)
        self.output('  Demo  :  generate')
        self.output('')
