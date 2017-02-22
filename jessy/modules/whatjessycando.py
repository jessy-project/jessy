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

    def _describe_general(self, mods):
        '''
        Describe general skills (installed).
        '''
        out = []
        skills = []
        for mod in mods:
            plugin = importlib.import_module(mod).plugin
            if plugin.IS_SKILL:
                skills.append(plugin.NAME)
        out.append(Phrase().text('I can operate ' + ', '.join(sorted(skills[:-1])) + \
                                 ' and ' + skills[-1]))  ## Rip from the define module and turn into an util helper
        out.append(Phrase().text('Ask me what some of these can do.'))
        return out

    def _describe_skill(self, mods, skill):
        '''
        Describe an exact skill
        '''
        out = []
        for mod in mods:
            plugin = importlib.import_module(mod).plugin
            if skill.lower() == plugin.NAME.lower():
                out.append(Phrase().text(plugin.DESCR))
                break
        return out
        

    def _handle(self, transcription):
        '''
        Scan modules, list stuff.
        '''
        target_module = transcription.lower()
        # Remove general words
        # This is going to be used "What foo can do?" where "foo" is found skill.
        for w in self.keywords() + ['you']:
            target_module = target_module.replace(w, '').strip()

        mods = set()
        pth = os.path.dirname(__file__)
        for mod in os.listdir(pth):
            if mod.startswith('_') \
               or os.path.isdir(os.path.join(pth, mod)) \
               or mod.startswith(os.path.basename(__file__).split('.')[0]):
                continue
            mod = mod.split('.')[0].strip()
            if mod:
                mods.add(mod)

        out = self._describe_skill(mods, target_module) if target_module else self._describe_general(mods)
        self.say(out)
        return bool(out)

    def handle(self, transcription, context=None):
        '''
        Handle query.
        '''
        state = False
        if all_words(transcription.lower(), *self.keywords(), exact=True):
            state = self._handle(transcription)
        return state

    def context(self):
        '''
        Save the context, if needed.
        '''
        return self.NAME

    @classmethod
    def keywords(cls):
        return ['what', 'can', 'do']


plugin = WhatJessyCanDo
