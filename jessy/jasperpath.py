# -*- coding: utf-8-*-
import os
import jessy

APP_PATH = LIB_PATH = jessy.__path__[0]
DATA_PATH = os.path.join(os.environ.get('VIRTUAL_ENV', '/usr'), "share/jessy/static")
PLUGIN_PATH = os.path.join(LIB_PATH, "modules")
CONFIG_PATH = os.path.expanduser(os.getenv('JASPER_CONFIG', '{0}/.jessy'.format(os.path.expanduser('~'))))


def config(*fname):
    '''
    Get config path.
    '''
    return os.path.join(CONFIG_PATH, *fname)


def data(*fname):
    '''
    Get path of the static data
    '''
    return os.path.join(DATA_PATH, *fname)
