# -*- coding: utf-8 -*-
# Copyright (C)2014 DKRZ GmbH

"""Recipe conda"""

def install_pkgs(home, pkgs, channel=None):
    from subprocess import check_call
    import os
    
    pkgs = pkgs.strip()
    if not pkgs:
        return
    if pkgs:
        lines = pkgs.split('\n')
        lines = [l.strip() for l in lines]

        cmd = [os.path.join(home, 'bin/conda')]
        cmd.append('install')
        if channel is not None:
            cmd.append('-c')
            cmd.append(channel)
        for line in lines:
            pkg_list = line.split(' ')
            pkg_list = [pkg.strip() for pkg in pkg_list]
            cmd.extend(pkg_list)
        check_call(cmd, shell=False)
        
class Conda(object):
    """This recipe is used by zc.buildout"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']
        self.anaconda_home = b_options.get('anaconda-home', '/opt/anaconda')
        self.conda_channel = b_options.get('conda-channel')
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
        install_pkgs(self.anaconda_home, pkgs, self.conda_channel) 

def uninstall(name, options):
    pass

