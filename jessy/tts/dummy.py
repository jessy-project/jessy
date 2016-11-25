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

import argparse
import yaml

from jessy import diagnose
from jessy import jasperpath
from jessy.utils import _module_getter
from jessy.tts import AbstractTTSEngine


def is_valid():
    '''
    Validator.
    '''
    return True


initiator = _module_getter(DummyTTS)


class DummyTTS(AbstractTTSEngine):
    """
    Dummy TTS engine that logs phrases with INFO level instead of synthesizing
    speech.
    """

    SLUG = "dummy-tts"

    @classmethod
    def is_available(cls):
        return True

    def say(self, phrase):
        self._logger.info(phrase)

    def play(self, filename):
        self._logger.debug("Playback of file '%s' requested")
        pass
