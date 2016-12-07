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

import os
import nltk

# Setup environment for NLTK
from jessy.modules.lib import nltkdata
os.environ['NLTK_DATA'] = nltkdata.__path__[0]
nltk.data.path.append(os.environ['NLTK_DATA'])


class Language(object):
    '''
    Supported languages
    '''
    ENGLISH = 'english'

    @classmethod
    def _get_languages(cls):
        return [lng for ln_name, lng in cls.__dict__.items() if not ln_name.startswith('_')]


class Tokeniser(object):
    '''
    Tokenise natural language and tag each word.
    '''

    def __init__(self, language):
        '''
        Init
        :param language:
        '''
        if language in Language._get_languages():
            self.__language = language
        else:
            raise Exception("Language '{}' is unsupported".format(language))

    def tokenise(self, text):
        '''
        Tokenise text.

        :param text:
        :return:
        '''
        return nltk.word_tokenize(text, self.__language)

    def tag(self, text):
        '''
        Tag words
        :param text:
        :return:
        '''
        return nltk.pos_tag(self.tokenise(text))
