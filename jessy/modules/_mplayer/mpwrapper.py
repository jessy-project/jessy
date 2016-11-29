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
import shutil
import tempfile


class MPlayer(object):
    '''
    MPlayer wrapper.
    '''
    def __init__(self):
        self._cmd = 'mplayer -really-quiet -slave -input file={fifo} {url}'
        self._station = ''
        self._process = None
        self._fifo = None
        self._volume = 100

    def _volume(method):
        '''
        Volume decorator.
        '''
        def postprocess(self):
            method(self)
            print "Setting volume to", self._volume, "at", id(self)
            self._fifo.write('volume {0} 1\n'.format(self._volume))
        return postprocess

    def _cleanup(method):
        '''
        Ensure to wipe out the reference to the sub-process after termination.
        '''
        def postprocess(self):
            method(self)
            self._process = None
            self._remove_fifo()
        return postprocess

    def _create_fifo(self):
        '''
        Create a fifo file for controlling MPlayer.
        '''
        if not self._fifo:
            fifo_path = os.path.join(tempfile.mkdtemp(), '.mplayer.fifo')
            try:
                os.mkfifo(fifo_path)
                self._fifo = open(fifo_path, 'w+', 0)
            except OSError as ex:
                print "Error creating control fifo"

        return self._fifo.name

    def _remove_fifo(self):
        '''
        Remove fifo
        '''
        if self._fifo:
            self._fifo.close()
            shutil.rmtree(os.path.dirname(self._fifo.name))
            self._fifo = None

    def _is_running(self):
        '''
        Check if process is running.
        '''
        if self._process:
            print "Check:", self._process.pid
            try:
                os.kill(self._process.pid, 0)
            except OSError as ex:
                return False
        return True

    @property
    def station(self):
        return self._station

    @station.setter
    def station(self, value):
        if value.startswith('http'):
            self._station = value

    @_volume
    def play(self):
        if self._process is None:
            if self.station:
                fifo_path = self._create_fifo()
                if fifo_path:
                    self._process = subprocess.Popen(self._cmd.format(fifo=fifo_path, url=self.station),
                                                     stdin=subprocess.PIPE,
                                                     stdout=open('/dev/null', 'w'),
                                                     stderr=open('/dev/null', 'w'),
                                                     shell=True, preexec_fn=os.setsid)
                    if self._is_running():
                        self._volume = 100
            else:
                print "Error: no station selected"
        else:
            print "Error: Already playing"

    @_cleanup
    def stop(self):
        if self._process is not None:
            self._fifo.write('stop\n')

    @_volume
    def quieter(self):
        if self._volume - 25 < 0:
            self._volume = 0
        else:
            self._volume -= 25

    @_volume
    def louder(self):
        if self._volume + 25 < 100:
            self._volume += 25
        else:
            self._volume = 100

    @_volume
    def background(self):
        self._volume /= 2

    @_volume
    def foreground(self):
        self._volume *= 2

    def mute(self):
        self._fifo.write('volume 0 1\n')

    @_volume
    def unmute(self):
        pass

    @_cleanup
    def kill(self):
        '''
        Force kill the process.
        '''
        if self._process is not None:
            os.killpg(os.getpgid(self._process.pid), signal.SIGTERM)
