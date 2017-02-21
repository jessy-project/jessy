# -*- coding: utf-8-*-
import random
from jessy.modules import JessyModule, all_words, Phrase
import os
import importlib


class WhatJessyCanDo(JessyModule):
    '''
    What you can do?
    '''
    NAME = 'Skills inspector'

    def __init__(self, *args, **kwargs):
        JessyModule.__init__(self, *args, **kwargs)

    def _handle(self, transcription, general=True):
        '''
        Scan modules, list stuff.
        '''
        target_module = transcription.lower()
        # Remove general words
        # This is going to be used "What foo can do?" where "foo" is found skill.
        for w in self.keywords():
            target_module = target_module.replace(w, '')

        mods = set()
        pth = os.path.dirname(__file__)
        for mod in os.listdir(pth):
            if mod.startswith('_') \
               or os.path.isdir(os.path.join(pth, mod)) \
               or mod.startswith(os.path.basename(__file__).split('.')[0]):
                continue
            mods.add(mod.split('.')[0])

        out = []

        skills = []
        for mod in mods:
            if not mod:
                continue
            plugin = importlib.import_module(mod).plugin
            if plugin.IS_SKILL:
                skills.append(plugin.NAME)
        out.append(Phrase().text('I can operate ' + ', '.join(sorted(skills[:-1])) + \
                                 ' and ' + skills[-1]))  ## Rip from the define module and turn into an util helper

        self.say(out)
        return True

    def handle(self, transcription):
        if all_words(transcription.lower(), *self.keywords() + ['you'], exact=True):
            return self._handle(transcription)
        elif all_words(transcription.lower(), *self.keywords(), exact=True):
            return self._handle(transcription, general=False)
        else:
            print ">>>", transcription, "is not", self.keywords()
        return True

    @classmethod
    def keywords(cls):
        return ['what', 'can', 'do']


plugin = WhatJessyCanDo
