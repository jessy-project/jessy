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
import yaml
import time
import os


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
                    raise Exception('Authentication error to {0}'.format(self.__url))


class SUSEManager(JessyModule):
    '''
    SUSE Manager communication module.
    '''
    NAME = 'Manager'
    DESCR = 'Allows to get generic information from connected SUSE Manager.'
    API = 'suma-api'

    def __init__(self, *args, **kwargs):
        JessyModule.__init__(self, *args, **kwargs)
        self.status_tpl = (
            ('users', 'there {are_is} {val} user{pl}'),
            ('systems', 'of known {val} system{pl}'),
            ('channels', 'and {are_is} {val} channel{pl} to use'),
            ('advisories', '{val} advisory{pl}'),  # Technically typo "advisorys"
                                                   # but sounds on the synthesizer right.
            ('affected_channels', 'however {val} channel{pl} needs patches'),
            ('affected_machines', 'and {val} machine{pl} needs updates'),
        )
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
        changed = False
        # Shortcuts
        def ph(text):    # Creates phrase
            return Phrase().text(text)
        def pl(amount):  # English plurals
            return amount and 's' or ''

        out = [ph('status')]
        is_full = status.get('is_full')
        if 'is_full' in status:
            del status['is_full']

        if is_full:
            out.append(ph('of suse manager'))
            for t_key, t_label in self.status_tpl:
                st_val = status.get(t_key)
                if st_val:
                    out.append(ph(t_label.format(val=st_val, pl=pl(st_val),
                                                 are_is=(st_val > 1 and 'are' or 'is'))))
            if not status:
                out.append(ph('unknown'))
        else:
            if not status:
                out.append(ph('unchanged'))
            else:
                changed = True
                out.append(ph('changed to'))
                for t_key, t_label in self.status_tpl:
                    st_val = status.get(t_key)
                    if st_val:
                        out.append(ph(t_label.format(val=st_val, pl=pl(st_val),
                                                     are_is=(st_val > 1 and 'are' or 'is'))))
        status['is_full'] = bool(is_full)
        self.say(out)
        return changed

    def _save_status(self, status):
        '''
        Saves status to the destination directory.
        '''
        t_path = self._config.get('reports')
        if not t_path:  # We are not saving anything
            return

        #del status['is_full']
        with open(os.path.join(t_path, str(int(time.time())) + '.yml'), 'w') as report:
            report.write(yaml.dump(status, default_flow_style=False) + os.linesep)

    def _compare_status(self, status):
        '''
        Compare data with the latest status.
        '''
        # Not implemented yet
        return status


    def handle(self, transcription, context=None):
        if self.matches(transcription):
            self.say('It might take a bit')
            status = self._compare_status(self._get_dashboard_status())
            self.say('OK, got it.')
            self._say_dashboard_status(status)

            return True

    @classmethod
    def keywords(cls):
        return ['manager', 'status']


plugin = SUSEManager
