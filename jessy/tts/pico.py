# -*- coding: utf-8-*-
"""
A Speaker handles audio output from Jasper to the user

Speaker methods:
    say - output 'phrase' as speech
    play - play the audio in 'filename'
    is_available - returns True if the platform supports this implementation
"""
import os
import re
import tempfile
import subprocess
import pipes

from jessy import diagnose
from jessy import jessypath
from jessy.utils import _module_getter
from jessy.tts import AbstractTTSEngine


class PicoTTS(AbstractTTSEngine):
    """
    Uses the svox-pico-tts speech synthesizer
    Requires pico2wave to be available
    """

    SLUG = "pico-tts"

    def __init__(self, language="en-US"):
        super(self.__class__, self).__init__()
        self.language = language

    @classmethod
    def is_available(cls):
        return (super(cls, cls).is_available() and
                diagnose.check_executable('pico2wave'))

    @classmethod
    def get_config(cls, profile):
        config = {}
        if 'pico-tts' in profile and 'language' in profile['pico-tts']:
            config['language'] = profile['pico-tts']['language']

        return config

    @property
    def languages(self):
        cmd = ['pico2wave', '-l', 'NULL',
                            '-w', os.devnull,
                            'NULL']
        with tempfile.SpooledTemporaryFile() as f:
            subprocess.call(cmd, stderr=f)
            f.seek(0)
            output = f.read()
        pattern = re.compile(r'Unknown language: NULL\nValid languages:\n' +
                             r'((?:[a-z]{2}-[A-Z]{2}\n)+)')
        matchobj = pattern.match(output)
        if not matchobj:
            raise RuntimeError("pico2wave: valid languages not detected")
        langs = matchobj.group(1).split()
        return langs

    def say(self, phrase, *args):
        self._logger.debug("Saying '%s' with '%s'", phrase, self.SLUG)
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            fname = f.name
        cmd = ['pico2wave', '--wave', fname]
        if self.language not in self.languages:
                raise ValueError("Language '%s' not supported by '%s'",
                                 self.language, self.SLUG)
        cmd.extend(['-l', self.language])
        cmd.append(phrase)
        self._logger.debug('Executing %s', ' '.join([pipes.quote(arg)
                                                     for arg in cmd]))
        with tempfile.TemporaryFile() as f:
            subprocess.call(cmd, stdout=f, stderr=f)
            f.seek(0)
            output = f.read()
            if output:
                self._logger.debug("Output was: '%s'", output)
        self.play(fname)
        os.remove(fname)


def is_valid():
    '''
    Validator.
    '''
    return True


initiator = _module_getter(PicoTTS)
