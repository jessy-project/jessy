# -*- coding: utf-8-*-
"""
A Speaker handles audio output from Jasper to the user

Speaker methods:
    say - output 'phrase' as speech
    play - play the audio in 'filename'
    is_available - returns True if the platform supports this implementation
"""
from jessy.utils import _module_getter
from jessy.tts import AbstractTTSEngine


class DummyTTS(AbstractTTSEngine):
    """
    Dummy TTS engine that logs phrases with INFO level instead of synthesizing
    speech.
    """

    SLUG = "dummy-tts"

    @classmethod
    def is_available(cls):
        return True

    def say(self, phrase, *args):
        self._logger.info(phrase)

    def play(self, filename):
        self._logger.debug("Playback of file '%s' requested")
        pass


def is_valid():
    '''
    Validator.
    '''
    return True


initiator = _module_getter(DummyTTS)
