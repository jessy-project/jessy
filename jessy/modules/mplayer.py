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

from jessy.modules import JessyModule, all_words
from jessy.modules._mplayer.mpwrapper import MPlayer


class MPlayerWrapper(JessyModule):
    '''
    MPlayer Wrapper
    '''
    def __init__(self, *args, **kwargs):
        JessyModule.__init__(self, *args, **kwargs)
        self._stopped = False
        self._process_registry.add_process(self._process_registry.Groups.MUSIC,
                                           'mplayer', MPlayer())

    def _get_mp(self):
        '''
        Get registered process.

        :return:
        '''
        return self._process_registry.process(self._process_registry.Groups.MUSIC, 'mplayer')

    def _handle(self, text):
        '''
        Handles the whole thing.

        :param mic:
        :param profile:
        :return:
        '''
        self._stopped = False
        self._get_mp().station = "http://us1.internet-radio.com:11094/"
        if all_words(text, 'stop') or all_words(text, 'shut', 'up'):
            self._get_mp().stop()
            self._mic.say("Stopped")
            self._stopped = True
        elif all_words(text, 'quieter') or all_words(text, 'more', 'quiet'):
            self._get_mp().quieter()
        elif all_words(text, 'louder') or all_words(text, 'more', 'loud'):
            self._get_mp().louder()
        elif all_words(text, 'mute', exact=True):
            self._get_mp().mute()
        elif all_words(text, 'unmute', exact=True):
            self._get_mp().unmute()
        else:
            self._get_mp().play()
            self._mic.say("Playing")

    def handle(self, transcription):
        '''
        Handle the whole thing.

        :param transcription:
        :return:
        '''
        if self.matches(transcription):
            self._handle(transcription.lower())
            return True

    def context(self):
        '''
        Save context
        :return:
        '''
        return not self._stopped and self.keywords() or []

    @classmethod
    def keywords(cls):
        return ['online', 'radio']  # Any! Todo: Should be "all of them" for context.


plugin = MPlayerWrapper
