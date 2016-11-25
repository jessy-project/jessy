# -*- coding: utf-8-*-
"""
A Speaker handles audio output from Jasper to the user

Speaker methods:
    say - output 'phrase' as speech
    play - play the audio in 'filename'
    is_available - returns True if the platform supports this implementation
"""
import os
import platform
import re
import tempfile
import subprocess
import pipes
import logging
import wave
import urllib
import urlparse
import requests
from abc import ABCMeta, abstractmethod

from jessy import diagnose
from jessy import jasperpath
from jessy.utils import _module_getter
from jessy.tts import AbstractTTSEngine


def is_valid():
    '''
    Validator.
    '''
    return True


initiator = _module_getter(MacOSXTTS)


class MacOSXTTS(AbstractTTSEngine):
    """
    Uses the OS X built-in 'say' command
    """

    SLUG = "osx-tts"

    @classmethod
    def is_available(cls):
        return (platform.system().lower() == 'darwin' and
                diagnose.check_executable('say') and
                diagnose.check_executable('afplay'))

    def say(self, phrase):
        self._logger.debug("Saying '%s' with '%s'", phrase, self.SLUG)
        cmd = ['say', str(phrase)]
        self._logger.debug('Executing %s', ' '.join([pipes.quote(arg)
                                                     for arg in cmd]))
        with tempfile.TemporaryFile() as f:
            subprocess.call(cmd, stdout=f, stderr=f)
            f.seek(0)
            output = f.read()
            if output:
                self._logger.debug("Output was: '%s'", output)

    def play(self, filename):
        cmd = ['afplay', str(filename)]
        self._logger.debug('Executing %s', ' '.join([pipes.quote(arg)
                                                     for arg in cmd]))
        with tempfile.TemporaryFile() as f:
            subprocess.call(cmd, stdout=f, stderr=f)
            f.seek(0)
            output = f.read()
            if output:
                self._logger.debug("Output was: '%s'", output)
