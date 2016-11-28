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
import signal
import subprocess
import time


class MPlayer(object):
    '''
    MPlayer wrapper.
    '''
    def __init__(self):
        self._cmd = 'mplayer -really-quiet {0}'
        self._station = ''
        self._process = None

    def _cleanup(method):
        '''
        Ensure to wipe out the reference to the sub-process after termination.
        '''
        def postprocess(self):
            method(self)
            self._process = None
        return postprocess

    @property
    def station(self):
        return self._station

    @station.setter
    def station(self, value):
        if value.startswith('http'):
            self._station = value

    def play(self):
        if self._process is None:
            if self.station:
                self._process = subprocess.Popen(self._cmd.format(self.station),
                                                 stdin=subprocess.PIPE,
                                                 stdout=open('/dev/null', 'w'),
                                                 stderr=open('/dev/null', 'w'),
                                                 shell=True, preexec_fn=os.setsid)
            else:
                print "Error: no station selected"
        else:
            print "Error: Already playing"

    @_cleanup
    def stop(self):
        if self._process is not None:
            self._process.communicate('q')

    @_cleanup
    def kill(self):
        '''
        Force kill the process.
        '''
        if self._process is not None:
            os.killpg(os.getpgid(self._process.pid), signal.SIGTERM)
