# -*- coding: utf-8-*-

'''
Main class
'''

import logging

from jessy import tts
from jessy import stt
from jessy import jessypath
from jessy import diagnose
from jessy.conversation import Conversation
from jessy.lazyload import LazyLoad
from jessy import config


class Jessy(object):
    '''
    Main class.
    '''
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._stt = LazyLoad().scan('jessy.stt')
        self._tts = LazyLoad().scan('jessy.tts')
        self.config = {}
        self.mic = None

    def get_stt_modules(self):
        '''
        Return available STT modules.
        '''
        return self._stt.modules()

    def get_tts_modules(self):
        '''
        Return available TTS modules.
        '''
        return self._tts.modules()

    def initialize(self, mic):
        '''
        Initialize Jessy.

        :param mic:
        :return:
        '''

        self.config = config.load_config(jessypath.CONFIG_PATH)

        stt_engine_class = self._stt[self.config['stt_engine']].initiator()
        if 'stt_passive_engine' in self.config:
            stt_passive_engine_class = self._stt[self.config['stt_passive_engine']].initiator()
        else:
            stt_passive_engine_class = stt_engine_class

        tts_engine_class = self._tts[self.config['tts_engine']].initiator()

        # Initialize Mic
        self.mic = mic(tts_engine_class.get_instance(self.config),
                       stt_passive_engine_class.get_passive_instance(self.config),
                       stt_engine_class.get_active_instance(self.config))
        return self

    def run(self):
        if 'first_name' in self.config:
            salutation = "Hey, {0}. Glad to see you. How can I help you?".format(self.config["first_name"])
        else:
            salutation = "How can I help you?"
        self.mic.say(salutation)

        Conversation(self.config.get('persona', 'jasper').upper(),
                     self.mic, self.config).handle_forever()
