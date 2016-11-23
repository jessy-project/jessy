# -*- coding: utf-8-*-
import random
import re

WORDS = ["WHY", "HOW"]


def handle(text, mic, profile):
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


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bhello\b', text, re.IGNORECASE))
