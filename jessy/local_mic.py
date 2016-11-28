# -*- coding: utf-8-*-
"""
A drop-in replacement for the Mic class that allows for all I/O to occur
over the terminal. Useful for debugging. Unlike with the typical Mic
implementation, Jasper is always active listening with local_mic.
"""


class Mic:
    prev = None

    def __init__(self, speaker, passive_stt_engine, active_stt_engine):
        '''
        Initialize local mic
        '''

    def passive_listen(self, persona):
        '''
        Passive listener.
        '''
        return True, persona

    def active_listen_to_all_options(self, THRESHOLD=None, LISTEN=True, MUSIC=False):
        '''
        Active listener (all opts)
        '''
        return [self.active_listen(THRESHOLD=THRESHOLD, LISTEN=LISTEN, MUSIC=MUSIC)]

    def active_listen(self, THRESHOLD=None, LISTEN=True, MUSIC=False):
        '''
        Active listener
        '''
        if not LISTEN:
            return self.prev

        input = None
        prompt = 'YOU'
        while not input:
            input = raw_input("{0}: ".format(prompt))
            prompt = '...'
        self.prev = input
        return input.upper()

    def say(self, phrase, OPTIONS=None):
        print ">>>: {0}".format(phrase)
