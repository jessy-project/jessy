# -*- coding: utf-8-*-
import datetime
import re
from jessy.app_utils import get_timezone as get_timezone
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
    Time alarm.
    '''
    NAME = 'Alarm'
    DESCR = 'Allows setup alarm at specific time'
    IS_SKILL = True

    def __init__(self, *args, **kwargs):
        JessyModule.__init__(self, *args, **kwargs)

    def handle(self, transcription):
        if self.matches(transcription):
            _handle(self._mic, self._config)
            return True

    @classmethod
    def keywords(cls):
        return ['time']


plugin = TimeAlarm
