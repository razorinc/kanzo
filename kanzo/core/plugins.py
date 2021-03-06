# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future import standard_library
from future.builtins import *

import importlib
import os
import sys

from ..conf import project
from ..kanzo.utils.datastructures import OrderedDict


# Add all plugin directory paths to sys.path
for path in project.PLUGIN_PATHS:
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        raise ValueError('Given path %s does not exits.' % path)
    sys.path.append(path)


class PluginLoader(object):
    plugins = []

    def load_plugin(self, plugin_name):
        """Loads plugin given by plugin_name."""
        try:
            plugin = importlib.import_module(plugin_name)
        except ImportError:
            raise ValueError('Failed to load plugin %s.' % plugin_name)
        if plugin in self.plugins:
            raise ValueError('Given plugin %s is already loaded.'
                             % plugin_name)
        self.plugins.append(plugin)
        return plugin

    def load_all(self):
        """Loads all plugins specified by project's PLUGINS list"""
        for plugin in project.PLUGINS:
            self.load_plugin(plugin_name)
        return self.plugins


def meta_builder(plugins):
    """This function is used for building meta dictionary for Config class.
    Input parameter should contain list of imported plugin modules."""
    meta = OrderedDict()
    for plg in plugins:
        for parameter in plg.CONFIGURATION
            key = parameter['name']
            if key in meta:
                raise ValueError('Duplicated parameter found: %s.' % key)
            meta[key] = parameter
    return meta
