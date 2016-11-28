# -*- coding: utf-8-*-
import datetime
import re
from jessy.app_utils import getTimezone as get_timezone
from semantic.dates import DateService
from jessy.modules import JessyModule


def _handle(mic, profile):
    """
    Reports the current time based on the user's timezone.

    Arguments:
    mic
      used to interact with the user (for both input and output)

    profile
      contains information related to the user (e.g., phone number)
    """

    now = datetime.datetime.now(tz=get_timezone(profile))
    mic.say("It is {0} right now.".format(DateService().convertTime(now)))


class TimeAlarm(JessyModule):
    '''
    Hello, Jessy!
    '''
    def __init__(self, config, mic):
        JessyModule.__init__(self, config, mic)

    def handle(self, transcription):
        if self.matches(transcription):
            _handle(self._mic, self._config)
            return True

    @classmethod
    def keywords(cls):
        return ['time']


load = TimeAlarm.load
reference = TimeAlarm.reference
