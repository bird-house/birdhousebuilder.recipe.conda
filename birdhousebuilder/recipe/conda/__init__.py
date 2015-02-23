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
    
    if len(pkgs) > 0:
        cmd = [os.path.join(home, 'bin/conda')]
        cmd.append('install')
        cmd.append('--yes')
        for channel in channels:
            cmd.append('-c')
            cmd.append(channel)
        cmd.extend(pkgs)
        check_call(cmd)
    return pkgs
        
class Recipe(object):
    """This recipe is used by zc.buildout"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']
        self.prefix = b_options.get('anaconda-home', anaconda_home())
        b_options['anaconda-home'] = self.prefix
        self.channels = split_args( b_options.get('conda-channels', 'pingucarsti birdhouse') )
        self.channels.extend( split_args( options.get('channels')) )
        self.on_update = as_bool(options.get('on-update', 'false'))
        self.pkgs = split_args(options.get('pkgs'))

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
        install_pkgs(self.prefix, self.pkgs, self.channels)
        
def uninstall(name, options):
    pass

