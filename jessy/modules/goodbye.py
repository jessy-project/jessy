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
from jessy.modules import JessyModule


class GoodBye(JessyModule):
    '''
    Goodbye module.
    '''
    NAME = 'Goodbye'
    DESCR = 'This is how I say goodbye to you or getting quiet.'

    def __init__(self, *args, **kwargs):
        JessyModule.__init__(self, *args, **kwargs)

    def handle(self, transcription, context=None):
        if self.matches(transcription):
            transcription = transcription.lower()
            if 'goodbye' in transcription:
                msg = choice(['Yep, bye', 'Good bye', 'Talk to you soon', 'Thank you, bye', 'See you'])
            elif 'shut' in transcription:
                msg = choice(['OK', 'No problem', 'Got it', 'Later'])
            elif 'quiet':
                msg = choice(['oh', 'uhm', 'huh?'])
            else:
                msg = 'See you'

            self._mic.say(msg)
            return True

    @classmethod
    def keywords(cls):
        return ['goodbye', 'quiet', 'shut', 'up', 'bye']


plugin = GoodBye
