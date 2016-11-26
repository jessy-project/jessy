# -*- coding: utf-8-*-
import os
import jessy
import logging

logger = logging.getLogger(__name__)

APP_PATH = LIB_PATH = jessy.__path__[0]
DATA_PATH = os.path.join(os.environ.get('VIRTUAL_ENV', '/usr'), "share/jessy/static")
PLUGIN_PATH = os.path.join(LIB_PATH, "modules")

# Set configuration path: personal or global
LOCAL_STORE = '{0}/.jessy'.format(os.path.expanduser('~'))
if not os.access(LOCAL_STORE, os.W_OK):
    logger.critical("Config dir {0} is not writable. Jessy won't work correctly.".format(LOCAL_STORE))

CONFIG_FILENAME = 'profile.conf'
CONFIG_PATH = os.path.join(os.path.expanduser(os.getenv('JESSY_CONFIG', LOCAL_STORE)), CONFIG_FILENAME)
if not os.path.exists(CONFIG_PATH):
    CONFIG_PATH = os.path.join('/etc/jessy', CONFIG_FILENAME)
    if not os.path.exists(CONFIG_PATH):
        CONFIG_PATH = None


def config(*fname):
    '''
    Get config path.
    '''
    return os.path.join(CONFIG_PATH or '', *fname)


def data(*fname):
    '''
    Get path of the static data
    '''
    return os.path.join(DATA_PATH, *fname)
