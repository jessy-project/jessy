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

from random import choice
from jessy.modules import JessyModule, all_words


class DecisionMaker(JessyModule):
    '''
    Decision maker
    '''
    NAME = 'Decision maker'
    DESCR = 'You can ask {0} to decide to do something or not'.format(NAME)
    IS_SKILL = True

    def __init__(self, *args, **kwargs):
        JessyModule.__init__(self, *args, **kwargs)
        self._long_prefixes = ['I decide that', 'If you ask, then I think', 'I suggest that',
                               'Stars says that', 'Aligning of quantum fluctuations shows that',
                               'Solar interference suggests that']
        self._short_prefixes = ['I think', 'In my opinion', 'To be honest',
                                'Actually', 'Kind of', 'I would say']
        self._decisions = ['it is a good idea', 'I would not go for it',
                           'I would not do that', 'sell it to somebody else, do not do this',
                           'grab it', 'it is surely a good idea',
                           'unlikely this will do any good to you',
                           'it is absolutely a good idea', 'it is no way',
                           'the answer would be certainly yes',
                           'this is a stupid thing to do. No, of course.',
                           'you should do it', 'you would better not do it',
                           'it is better to refrain from it', 'it is better to go with it']

    def handle(self, transcription, context=None):
        if self.matches(transcription):
            transcription = transcription.lower()
            if 'decide' in transcription or 'choose' in transcription:
                self.say('{0} {1}'.format(choice(self._long_prefixes), choice(self._decisions)))
            elif all_words(transcription, 'yes', 'or', 'no', 'not'):
                self.say('{0} {1}'.format(choice(self._short_prefixes), choice(['yes', 'no'])))
            return True

    @classmethod
    def keywords(cls):
        return ['decide', 'yes', 'or', 'not', 'no', 'choose']


plugin = DecisionMaker
