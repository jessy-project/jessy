# -*- coding: utf-8-*-
from sys import maxint
import random
from jessy.modules import JessyModule


def _handle(mic):
    """
        Reports that the user has unclear or unusable input.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """

    messages = [
        'I dit not understand',
        'I am probably deaf. Please repeat that.',
        'Oh but slowly, please. I am recording.',
        'Sorry. I missed that, because I am not a human.',
        'I am still a machine, not a human. Please say that again.',
        'Pardon?',
        'Uhm. I did not get that.',
        'Excuse me, what did you just said?',
    ]

    mic.say(random.choice(messages))


class _NoIdea(JessyModule):
    '''
    Handle GMail
    '''
    PRIORITY = -(maxint + 1)

    def __init__(self, config, mic):
        JessyModule.__init__(self, config, mic)

    def handle(self, transcription):
        _handle(self._mic)
        return True

    @classmethod
    def keywords(cls):
        return []

plugin = _NoIdea
