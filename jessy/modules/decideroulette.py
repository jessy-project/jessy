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

    def __init__(self, *args, **kwargs):
        JessyModule.__init__(self, *args, **kwargs)

    def handle(self, transcription):
        msg = None
        if self.matches(transcription):
            transcription = transcription.lower()
            if 'decide' in transcription or 'choose' in transcription:
                msg = choice(['I think it is a good idea', 'I would not go for it',
                              'I would not do that', 'sell it to somebody else, do not do this',
                              'grab it', 'it is surely a good idea',
                              'unlikely this will do any good to you',
                              'absolutely', 'no way', 'certainly yes',
                              'What a stupid thing do to. No, of course!',
                              'Of course do it! Why even question that!'])
            elif all_words(transcription, 'yes', 'or', 'no', 'not'):
                msg = choice(['yes', 'no'])

            self._mic.say(msg)
            return True

    @classmethod
    def keywords(cls):
        return ['decide', 'yes', 'or', 'not', 'no', 'choose']


plugin = DecisionMaker
