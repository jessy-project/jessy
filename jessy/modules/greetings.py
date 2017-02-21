# -*- coding: utf-8-*-
import random
from jessy.modules import JessyModule


def _handle(mic):
    """
        Responds to user-input, typically speech text, by relaying the
        meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    messages = ["Who are you? But hello anyway.",
                "Oh yeah. Hi there",
                "Hello to you too. But piss off. Please"]
    message = random.choice(messages)
    mic.say(message)


class HelloJessy(JessyModule):
    '''
    Hello, Jessy!
    '''
    NAME = 'Greetings'
    DESCR = 'Says greetings'

    def __init__(self, *args, **kwargs):
        JessyModule.__init__(self, *args, **kwargs)

    def handle(self, transcription):
        if self.matches(transcription):
            _handle(self._mic)
            return True

    @classmethod
    def keywords(cls):
        return ['hello']


plugin = HelloJessy
