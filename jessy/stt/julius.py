# -*- coding: utf-8-*-
import os
import tempfile
import logging
import re
import subprocess
import yaml

from jessy import jessypath
from jessy import diagnose
from jessy.utils import _module_getter
from jessy.stt import AbstractSTTEngine
from jessy.stt.lib import vocabcompiler


class JuliusSTT(AbstractSTTEngine):
    """
    A very basic Speech-to-Text engine using Julius.
    """

    SLUG = 'julius'
    VOCABULARY_TYPE = vocabcompiler.JuliusVocabulary

    def __init__(self, vocabulary=None, hmmdefs="/usr/share/voxforge/julius/" +
                 "acoustic_model_files/hmmdefs", tiedlist="/usr/share/" +
                 "voxforge/julius/acoustic_model_files/tiedlist"):
        self._logger = logging.getLogger(__name__)
        self._vocabulary = vocabulary
        self._hmmdefs = hmmdefs
        self._tiedlist = tiedlist
        self._pattern = re.compile(r'sentence(\d+): <s> (.+) </s>')

        # Inital test run: we run this command once to log errors/warnings
        cmd = ['julius',
               '-input', 'stdin',
               '-dfa', self._vocabulary.dfa_file,
               '-v', self._vocabulary.dict_file,
               '-h', self._hmmdefs,
               '-hlist', self._tiedlist,
               '-forcedict']
        cmd = [str(x) for x in cmd]
        self._logger.debug('Executing: %r', cmd)
        with tempfile.SpooledTemporaryFile() as out_f:
            with tempfile.SpooledTemporaryFile() as f:
                with tempfile.SpooledTemporaryFile() as err_f:
                    subprocess.call(cmd, stdin=f, stdout=out_f, stderr=err_f)
            out_f.seek(0)
            for line in out_f.read().splitlines():
                line = line.strip()
                if len(line) > 7 and line[:7].upper() == 'ERROR: ':
                    if not line[7:].startswith('adin_'):
                        self._logger.error(line[7:])
                elif len(line) > 9 and line[:9].upper() == 'WARNING: ':
                    self._logger.warning(line[9:])
                elif len(line) > 6 and line[:6].upper() == 'STAT: ':
                    self._logger.debug(line[6:])

    @classmethod
    def get_config(cls, profile):
        config = {}
        if 'julius' in profile:
            if 'hmmdefs' in profile['julius']:
                config['hmmdefs'] = profile['julius']['hmmdefs']
            if 'tiedlist' in profile['julius']:
                config['tiedlist'] = profile['julius']['tiedlist']

        return config

    def transcribe(self, fp, mode=None):
        cmd = ['julius',
               '-quiet',
               '-nolog',
               '-input', 'stdin',
               '-dfa', self._vocabulary.dfa_file,
               '-v', self._vocabulary.dict_file,
               '-h', self._hmmdefs,
               '-hlist', self._tiedlist,
               '-forcedict']
        cmd = [str(x) for x in cmd]
        self._logger.debug('Executing: %r', cmd)
        with tempfile.SpooledTemporaryFile() as out_f:
            with tempfile.SpooledTemporaryFile() as err_f:
                subprocess.call(cmd, stdin=fp, stdout=out_f, stderr=err_f)
            out_f.seek(0)
            results = [(int(i), text) for i, text in
                       self._pattern.findall(out_f.read())]
        transcribed = [text for i, text in
                       sorted(results, key=lambda x: x[0])
                       if text]
        if not transcribed:
            transcribed.append('')
        self._logger.info('Transcribed: %r', transcribed)
        return transcribed

    @classmethod
    def is_available(cls):
        return diagnose.check_executable('julius')


def is_valid():
    '''
    Module validator.
    '''
    return True


initiator = _module_getter(JuliusSTT)

