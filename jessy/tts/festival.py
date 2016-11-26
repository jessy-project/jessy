# -*- coding: utf-8-*-
"""
A Speaker handles audio output from Jasper to the user

Speaker methods:
    say - output 'phrase' as speech
    play - play the audio in 'filename'
    is_available - returns True if the platform supports this implementation
"""
import tempfile
import subprocess
import pipes
import logging

from jessy import diagnose
from jessy.utils import _module_getter
from jessy.tts import AbstractTTSEngine


class FestivalTTS(AbstractTTSEngine):
    """
    Uses the festival speech synthesizer
    Requires festival (text2wave) to be available
    """

    SLUG = 'festival-tts'

    @classmethod
    def is_available(cls):
        if (super(cls, cls).is_available() and
           diagnose.check_executable('text2wave') and
           diagnose.check_executable('festival')):

            logger = logging.getLogger(__name__)
            cmd = ['festival', '--pipe']
            with tempfile.SpooledTemporaryFile() as out_f:
                with tempfile.SpooledTemporaryFile() as in_f:
                    logger.debug('Executing %s', ' '.join([pipes.quote(arg)
                                                           for arg in cmd]))
                    subprocess.call(cmd, stdin=in_f, stdout=out_f,
                                    stderr=out_f)
                    out_f.seek(0)
                    output = out_f.read().strip()
                    if output:
                        logger.debug("Output was: '%s'", output)
                    return ('No default voice found' not in output)
        return False

    def say(self, phrase, *args):
        self._logger.debug("Saying '%s' with '%s'", phrase, self.SLUG)
        cmd = ['text2wave']
        with tempfile.NamedTemporaryFile(suffix='.wav') as out_f:
            with tempfile.SpooledTemporaryFile() as in_f:
                in_f.write(phrase)
                in_f.seek(0)
                with tempfile.SpooledTemporaryFile() as err_f:
                    self._logger.debug('Executing %s',
                                       ' '.join([pipes.quote(arg)
                                                 for arg in cmd]))
                    subprocess.call(cmd, stdin=in_f, stdout=out_f,
                                    stderr=err_f)
                    err_f.seek(0)
                    output = err_f.read()
                    if output:
                        self._logger.debug("Output was: '%s'", output)
            self.play(out_f.name)


def is_valid():
    '''
    Validator.
    '''
    return True


initiator = _module_getter(FestivalTTS)
