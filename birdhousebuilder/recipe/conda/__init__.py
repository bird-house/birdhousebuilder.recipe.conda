# -*- coding: utf-8 -*-
# Copyright (C)2014 DKRZ GmbH

"""Recipe conda"""

def as_bool(value):
    if value.lower() in ('1', 'true'):
        return True
    return False

def install_pkgs(pkgs):
    from subprocess import check_call
    
    pkgs = pkgs.strip()
    if not pkgs:
        return
    if pkgs:
        pkg_list = pkgs.split(' ')
        pkg_list = [l.strip() for l in pkg_list]
        for pkg in pkg_list:
            check_call('/opt/anaconda/bin/conda install -c https://conda.binstar.org/PinguCarsti %s' % (pkg), shell=True)
        
class Conda(object):
    """This recipe is used by zc.buildout"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.on_install = as_bool(options.get('on_install', 'false'))
        self.on_update = as_bool(options.get('on_update', 'false'))

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
        install_pkgs(pkgs) 

def uninstall(name, options):
    pass

