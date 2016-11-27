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
Abstract module interface
'''

from abc import ABCMeta, abstractmethod


class JessyModule(object):
    '''
    Interface to a Jessy module.
    '''
    __metaclass__ = ABCMeta
    PRIORITY = 0

    @abstractmethod
    def __init__(cls, config, mic):
        cls._config = config
        cls._mic = mic

    @abstractmethod
    def handle(cls, transcription):
        pass

    @staticmethod
    @abstractmethod
    @lowercase
    def keywords():
        return []

    def matches(self, text):
        '''
        Return True if incoming text has any of the words,
        returned by self.matches method.

        :return:
        '''
        for word in text.split(' '):
            word = word.lower()
            for match in self.keywords():
                if match in word:
                    return True

        return False

    @classmethod
    def load(cls, *args, **kwargs):
        '''
        Launcher function

        :param cls:
        :return:
        '''

        if type(cls) != type(JessyModule):
            raise TypeError('Launched module is a wrong type. '
                            'Should be a subclass of JessyModule.')
        return cls(*args, **kwargs)

    @classmethod
    def reference(cls):
        '''
        Reference a class
        :return:
        '''
        if type(cls) != type(JessyModule):
            raise TypeError('Referenced module is a wrong type. '
                            'Should be a subclass of JessyModule.')
        return cls
