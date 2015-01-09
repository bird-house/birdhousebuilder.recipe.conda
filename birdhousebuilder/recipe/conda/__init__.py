# -*- coding: utf-8 -*-
# Copyright (C)2014 DKRZ GmbH

"""Recipe conda"""

import os

def anaconda_home():
    return os.path.join(os.environ.get('HOME', ''), "anaconda")

def as_bool(value):
    if value.lower() in ('1', 'true'):
        return True
    return False

def makedirs(dirname):
    try:
        os.makedirs(dirname)
    except OSError:
        pass

def split_args(args):
    if args is None:
        return []
    
    all_args = []
    args = args.strip()
    if args:
        lines = args.split('\n')
        lines = [l.strip() for l in lines]
        for line in lines:
            arg_list = line.split(' ')
            arg_list = [arg.strip() for arg in arg_list]
            all_args.extend(arg_list)
    return all_args

def install_pkgs(home, pkgs, channels):
    from subprocess import check_call
    import os
    
    pkg_list = split_args(pkgs)
    if len(pkg_list) > 0:
        cmd = [os.path.join(home, 'bin/conda')]
        cmd.append('install')
        cmd.append('--yes')
        channel_list = split_args(channels)
        for channel in channel_list:
            cmd.append('-c')
            cmd.append(channel)
        cmd.extend(pkg_list)
        check_call(cmd)
    return pkg_list
        
class Recipe(object):
    """This recipe is used by zc.buildout"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']
        self.prefix = b_options.get('anaconda-home', anaconda_home())
        b_options['anaconda-home'] = self.prefix
        self.conda_channels = b_options.get('conda-channels', 'https://conda.binstar.org/pingucarsti https://conda.binstar.org/birdhouse')
        self.on_update = as_bool(options.get('on-update', 'false'))

    def install(self):
        """
        install conda packages
        """
        self.execute()
        return tuple()

    def update(self):
        if self.on_update:
            return self.execute()
        return tuple()

    def execute(self):
        pkgs = self.options.get('pkgs', '')
        install_pkgs(self.prefix, pkgs, self.conda_channels)
        

def uninstall(name, options):
    pass

