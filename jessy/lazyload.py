# -*- coding: utf-8-*-
#
# The MIT License (MIT)
#
# Copyright (c) 2016 Bogdan Maryniuk <bo@suse.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
Lazy loader of a Python files, found in particular path.
'''
import os
from importlib import import_module


class LoadModule(object):
    '''
    Module loader and mapper.
    '''
    def __init__(self, namespace, name):
        self._namespace = namespace
        self._name = name
        self._module = None

    def namespace(self):
        '''
        Show module namespace.
        '''
        return '{0}.{1}'.format(self._namespace, self._name)

    def get(self):
        '''
        Actually lazy-load a module.
        '''
        if self._module is None:
            self._module = import_module(self.namespace())

        return self._module


class LazyLoad(object):
    '''
    Lazy loader singleton.
    '''

    def __init__(self):
        self.__modules = {}

    def scan(self, namespace):
        '''
        Scan path.
        '''
        obj = import_module(namespace)
        path = (type(obj) == type('') and obj) or \
               (hasattr(obj, '__path__') and obj.__path__[0]) or None

        for mod in os.listdir(path):
            if mod.startswith("__"):
                continue
            else:
                name = mod.split('.')[0]
                self.__modules[name] = LoadModule(namespace, name)

        return self

    def __getitem__(self, name):
        '''
        Load a particular module.
        '''
        ref = self.__modules.get(name)
        if not ref:
            raise Exception("Module '{0}' not found".format(name))
        return ref.get()

    def modules(self):
        '''
        List available modules.
        '''
        modules = []
        for name in self.__modules.keys():
            modules.append(self.__modules[name].namespace())

        return sorted(modules)
