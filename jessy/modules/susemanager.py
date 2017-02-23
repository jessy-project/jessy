# -*- coding: utf-8-*-
#
# The MIT License (MIT)
#
# Copyright (c) 2017 Bogdan Maryniuk <bo@suse.de>
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

from random import choice
from jessy.modules import JessyModule, all_words, any_words, Phrase
import xmlrpclib


class APICall(object):
    def __init__(self, host, user, password):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__url = 'http://{0}/rpc/api'.format(host)
        self.__client = xmlrpclib.Server(self.__url, verbose=0)
        self.__token = ''

    def _auth(self):
        self.__token = self.__client.auth.login(self.__user, self.__password)

    def list_users(self):
        return self('user.list_users')

    def list_active_systems(self):
        return self('system.list_active_systems')

    def list_channels(self):
        return self('channel.list_all_channels')

    def list_patches(self, channel):
        return self('channel.software.list_errata', channel)

    def list_affected_systems(self, advisory):
        return self('errata.list_affected_systems')

    def list_subscribed_systems(self, channel):
        return self('channel.software.list_subscribed_systems', channel)

    def __call__(self, mtd, *args, **kwargs):
        for x in range(2):
            try:
                return getattr(self.__client, mtd)(self.__token, *args, **kwargs)
            except Exception as ex:
                try:
                    self._auth()
                except Exception as ex:
                    raise Exception('Authentication error to {0}'.format(self.__url)


class SUSEManager(JessyModule):
    '''
    SUSE Manager communication module.
    '''
    NAME = 'Manager'
    DESCR = 'Allows to get generic information from connected SUSE Manager.'
    API = 'suma-api'

    def __init__(self, *args, **kwargs):
        JessyModule.__init__(self, *args, **kwargs)
        self._config = self._config.get(self.module_name(__file__))
        self.register(self.API, APICall(self._config.get('host'),
                                        self._config.get('user'),
                                        self._config.get('password')))

    def _get_dashboard_status(self):
        '''
        Collect status from the dashboard.
        '''
        api = self.get_registry(self.API)

        # Get primary data
        _known_users = api.list_users()
        _active_systems = api.list_active_systems()
        _known_channels = api.list_channels()
        _known_advisories = {}
        _affected_channels = []

        for channel in _known_channels:
            patches = api.list_patches(channel['label'])
            if patches:
                _affected_channels.append(channel['label'])

        _affected_machines = {}
        for ch_label in _affected_channels:
            for machine in api.list_subscribed_systems(ch_label):
                _affected_machines['name'] = machine['name']
                _affected_machines['id'] = machine['id']

        return {'users': len(_known_users),
                'systems': len(_active_systems),
                'channels': len(_known_channels),
                'advisories': len(_known_advisories),
                'affected_channels': len(_affected_channels),
                'affected_machines': len(_affected_machines),
                'is_full': True,
        }

    def _say_dashboard_status(self, status):
        '''
        Say status of the dashboard.
        '''
        # Shortcuts
        def ph(text):    # Creates phrase
            return Phrase().text(text)
        def pl(amount):  # English plurals
            return amount and 's' or ''

        out = []
        is_full = status.get('is_full')
        del status['is_full']

        if is_full:
            out.append(ph('Status of SUSE Manager'))
            tpl = {'users': '{val} user{pl}',
                   'systems': 'known {val} system{pl}',
                   'channels': 'there {are_is} {val} channel{pl}',
                   'advisories': '{val} advisory{pl}',  # Technically typo "advisorys"
                                                        # but sounds on the synthesizer right.
                   'affected_channels': '{val} channel{pl} synchronized',
                   'affected_machines': 'Warning. {val} machine{pl} affected',
            }
            for st_key, st_val in status.items():
                if st_val:
                    out.append(ph(tpl[st_key].format(val=st_val, pl=pl(st_val),
                                                     are_is=(st_val > 1 and 'are' or 'is'))))
            if not status:
                out.append(ph('unknown'))
        else:                                # Says only difference from the last
            pass

        self.say(out)

    def _compare_status(self, status):
        '''
        Compare data with the latest status.
        '''
        # Not implemented yet
        return status


    def handle(self, transcription, context=None):
        if self.matches(transcription):
            self.say('Let me ask suse manager')
            self._say_dashboard_status(self._compare_status(self._get_dashboard_status()))

            return True

    @classmethod
    def keywords(cls):
        return ['manager', 'status']


plugin = SUSEManager
