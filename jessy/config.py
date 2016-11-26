# -*- coding: utf-8-*-
#
# The MIT License (MIT)
#
# Copyright (c) 2016 Bogdan Maryniuk <bo@suse.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
Configuration handler.
'''

import os
import time
import yaml
from jessy import jasperpath


CONFIG_NAME = 'profile.conf'
DEFAULT_CONFIG = {
    'persona': 'jessy',
    'carrier': '',
    'first_name': '',
    'last_name': '',
    'phone_number': '',
    'gmail_password': '',
    'prefers_email': False,
    'timezone': time.strftime('%Z', time.gmtime()),

    'stt_engine': 'pocketsphinx',
    'pocketsphinx': {
        'fst_model': '/home/pi/phono/g014b2b.fst',
        'hmm_dir': '/usr/share/pocketsphinx/model/hmm/en_US/hub4wsj_sc_8k',
    },

    'tts_engine': 'espeak',
    'espeak-tts': {
        'voice': 'en',
        'pitch_adjustment': 85,
        'words_per_minute': 100,
    }
}


def _deep_merge(src, dst):
    """
    Deep merge dictionaries.
    """
    for key, value in src.items():
        if type(value) == dict:
            _deep_merge(value, dst.setdefault(key, {}))
        else:
            dst[key] = value

    return dst


def load_config(path):
    '''
    Load configuration.

    :param path:
    :return:
    '''
    return path and os.path.exists(path) and _deep_merge(yaml.load(open(path).read()),
                                                         DEFAULT_CONFIG) or DEFAULT_CONFIG
