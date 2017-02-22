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
from jessy.modules import JessyModule
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
                self._auth()


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

    def handle(self, transcription, context=None):
        self.say('I am SUSE Manager')
        return True

    @classmethod
    def keywords(cls):
        return ['manager']


plugin = SUSEManager
