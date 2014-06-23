# -*- coding: utf-8 -*-
# Copyright (C)2014 DKRZ GmbH

"""Recipe conda"""

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
        channel_list = split_args(channels)
        for channel in channel_list:
            cmd.append('-c')
            cmd.append(channel)
        cmd.extend(pkg_list)
        check_call(cmd)
        
class Conda(object):
    """This recipe is used by zc.buildout"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']
        self.anaconda_home = b_options.get('anaconda-home', '/opt/anaconda')
        self.conda_channels = b_options.get('conda-channels')
        self.on_install = options.query_bool('on_install', default='false')
        self.on_update = options.query_bool('on_update', default='false')

    def install(self):
        """installer"""
        if self.on_install:
            self.execute()
        return tuple()

    def update(self):
        """updater"""
        if self.on_update:
            self.execute()
        return tuple()

    def execute(self):
        """run the commands
        """
        pkgs = self.options.get('pkgs', '')
        install_pkgs(self.anaconda_home, pkgs, self.conda_channels) 

def uninstall(name, options):
    pass

