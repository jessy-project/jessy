# -*- coding: utf-8-*-
import logging
import pkgutil
import os
from jessy import jessypath
from jessy.modules import is_valid_module


class SubProcessRegistry(object):
    '''
    Register a generally available subprocess registry.
    '''
    class Groups(object):
        MUSIC = 'music'
        SPEECH = 'speech'
        SYSTEM = 'system'

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.__groups = {}

    @property
    def groups(self):
        '''
        Returns available groups
        :return:
        '''
        return self.__groups.keys()[:]  # Internal store is immutable

    @groups.setter
    def group(self, value):
        '''
        Add a new group.

        :param value:
        :return:
        '''
        if value not in self.__groups:
            self.__groups[value] = {}

    def process(self, group, name):
        '''
        Get processes within a group.

        :param group:
        :return:
        '''
        return self.__groups.get(group, {}).get(name)

    def add_process(self, group, name, process):
        '''
        Set process to a group

        :param group:
        :param name:
        :param process:
        :return:
        '''
        self.group = group
        if self.__groups[group].get(name) is None:
            self.__groups[group][name] = process
            self._logger.debug("Added process '{0}@{1}'".format(name, group))

        return self

    def terminate_all(self):
        '''
        Terminate all processes.

        :return:
        '''
        for group in self.__groups.values():
            for name, process in group.items():
                try:
                    self._logger.debug("Terminating process "
                                       "'{0}@{1}'".format(name, group))
                    process.terminate()
                    self._logger.debug("Process '{0}@{1}' has been "
                                       "terminated".format(name, group))
                except Exception as ex:
                    self._logger.error("Error terminate process "
                                       "'{0}@{1}': {2}".format(name, group, ex))


class Brain(object):
    '''
    Main loop for conversation query.
    '''

    def __init__(self, mic, profile):
        """
        Instantiates a new Brain object, which cross-references user
        input with a list of modules. Note that the order of brain.modules
        matters, as the Brain will cease execution on the first module
        that accepts a given input.

        Arguments:
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
        """

        self.mic = mic
        self.profile = profile
        self.modules = self.get_modules()
        self._logger = logging.getLogger(__name__)
        self.process_registry = SubProcessRegistry()
        self._current_context = []

    @classmethod
    def get_modules(cls):
        """
        Dynamically loads all the modules in the modules folder and sorts
        them by the PRIORITY key. If no PRIORITY is defined for a given
        module, a priority of 0 is assumed.
        """

        logger = logging.getLogger(__name__)
        locations = list(set([jessypath.PLUGIN_PATH] + self.profile['modules']))
        logger.debug("Looking for modules in: %s", ', '.join(["'%s'" % location for location in locations]))
        modules = []
        for finder, name, ispkg in pkgutil.walk_packages(locations):
            if ispkg:
                continue
            try:
                mod = finder.find_module(name).load_module(name)
            except Exception as ex:
                logger.warning("Skipped module '{0}' due to an error: '{1}'".format(name, ex))
            else:
                if is_valid_module(mod):
                    logger.debug("Loading module '{0}'".format(name))
                    modules.append(mod)
                else:
                    logger.warning("Module '{0}' is invalid".format(name))

        modules.sort(key=lambda module: module.plugin.PRIORITY, reverse=True)
        return modules

    def in_context(self, text):
        '''
        Add current context.

        :param text:
        :return:
        '''

        return '{0} {1}'.format(' '.join(self._current_context), text).strip()

    def query(self, texts):
        """
        Passes user input to the appropriate module, testing it against
        each candidate module's isValid function.

        Arguments:
        text -- user input, typically speech, to be parsed by a module
        """
        for module in self.modules:
            for text in texts:
                try:
                    loader = module.plugin.load(config=self.profile,
                                                mic=self.mic,
                                                registry=self.process_registry)
                    if loader.handle(self.in_context(text)):
                        self._current_context = loader.context()
                        return
                except Exception as ex:
                    self._logger.error('Failed to execute module: {0}'.format(ex))
                    self.mic.say("I'm sorry. I had some trouble with that operation. Please try again later.")
                else:
                    self._logger.debug("Handling of phrase '%s' by module '%s' completed", text, module.__name__)
        self._logger.debug("No module was able to handle any of these phrases: %r", texts)
