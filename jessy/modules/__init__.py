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

import os
import time
from abc import ABCMeta, abstractmethod
from jessy.config import load_config


def lowercase(func):
    '''
    Convert output to uppercase

    :param func:
    :return:
    '''
    def caller(*args, **kwargs):
        '''
        Internal function caller

        :param args:
        :param kwargs:
        :return:
        '''
        return [word.lower() for word in func(*args, **kwargs)]

    return caller


def any_words(text, *words, **kwargs):
    '''
    Match any of specified words in the text.

    :param text:
    :param words:
    :param kwargs:
    :return:
    '''
    exact = bool(kwargs.get('exact'))
    for word in words:
        word = word.lower()
        for token in text.split(' '):
            token = token.lower()
            if (exact and token == word) or token.startswith(word):
                return True
    return False


def all_words(text, *words, **kwargs):
    '''
    Match all specified words in the text.

    :param text:
    :param words:
    :param kwargs:
    :return:
    '''
    exact = bool(kwargs.get('exact'))
    found = 0
    for word in words:
        for item in text.split(' '):
            if (exact and item == word) or item.startswith(word):
                found += 1

    return found and found == len(words)


def is_valid_module(mod):
    '''
    Check if module is valid.

    :param mod:
    :return:
    '''
    for ref in ['plugin']:
        if not hasattr(mod, ref):
            return False

    return True


def in_range(value, range):
    '''
    Keep an int within the range.

    :param value:
    :param range:
    :return:
    '''
    return (value <= 0 and 1 or value >= range and range + 1 or value + 1) - 1


# TODO: Move this to the mic generally available for everything
class Phrase(object):
    '''
    Prase for Mic articulation
    '''
    def __init__(self):
        self.__text = ''
        self.__pause = 0

    def text(self, value=None):
        if value:
            self.__text = value.split(os.linesep)[0]
            return self
        else:
            return self.__text

    def pause(self, value=None):
        if value:
            self.__pause = in_range(int(value), 3)
            return self
        else:
            return self.__pause


class JessyModule(object):
    '''
    Interface to a Jessy module.
    '''
    __metaclass__ = ABCMeta
    PRIORITY = 0

    @abstractmethod
    def __init__(cls, config, mic, registry):
        cls._config = load_config(cls.__module__, config)
        cls._mic = mic
        cls._process_registry = registry

    def say(self, text):
        '''
        An alias to the mic "say"

        :param text:
        :return:
        '''
        self._mic.say(text)

    @abstractmethod
    def handle(cls, transcription):
        pass

    @classmethod
    @abstractmethod
    @lowercase
    def keywords(cls):
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

    def context(self):
        '''
        Return True if context needs to be saved.
        The context of the module is the entry keywords.

        Every next input will be joined with the context.

        :return:
        '''
        return []