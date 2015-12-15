# -*- coding: utf-8 -*-

"""Recipe conda"""

import os
from os.path import join

def prefix():
    conda_envs_dir = os.environ.get('CONDA_ENVS_DIR', join(os.environ.get('HOME', ''), '.conda', 'envs'))
    # TODO: env should not be hard-coded
    return join(conda_envs_dir, 'birdhouse')

def anaconda_home():
    return os.environ.get('ANACONDA_HOME', join(os.environ.get('HOME', ''), 'anaconda'))

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

def env_exists(prefix, env=None):
    """returns True if environment exists otherwise False."""
    from subprocess import check_output
    
    if env is None or len(env.strip())==0:
        return True
    cmd = [join(prefix, 'bin', 'conda')]
    cmd.extend(['info', '-e'])
    output = check_output(cmd)
    found = False
    for line in output.splitlines():
        parts = line.split()
        if len(parts) == 0:
            continue
        if parts[0] == env:
            found = True
            break
    return found

def create_env(prefix, env=None, channels=[], pkgs=['python']):
    from subprocess import check_call

    if env_exists(prefix, env):
        return
    
    cmd = [join(prefix, 'bin', 'conda')]
    cmd.extend(['create', '-n', env])
    cmd.append('--yes')
    for channel in channels:
        cmd.append('-c')
        cmd.append(channel)
    cmd.extend(pkgs)
    check_call(cmd)

def install_pkgs(prefix, env=None, channels=[], pkgs=[]):
    from subprocess import check_call
    
    if len(pkgs) > 0:
        cmd = [join(prefix, 'bin', 'conda')]
        cmd.append('install')
        if env is not None:
            cmd.extend(['-n', env])
        cmd.append('--yes')
        for channel in channels:
            cmd.append('-c')
            cmd.append(channel)
        cmd.extend(pkgs)
        check_call(cmd)
    return pkgs
        
class Recipe(object):
    """This recipe is used by zc.buildout.
    It install conda packages."""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']
        # TODO: allow overwrite of anaconda_home
        self.anaconda_home = b_options.get('anaconda-home', anaconda_home())
        b_options['anaconda-home'] = self.anaconda_home
        self.prefix = b_options.get('prefix', prefix())
        b_options['prefix'] = self.prefix

        # offline mode
        self.offline = as_bool(b_options.get('offline', 'false'))
        
        self.channels = split_args( b_options.get('conda-channels', 'birdhouse ioos') )
        self.channels.extend( split_args( options.get('channels')) )
        # make channel list unique
        self.channels = list(set(self.channels))
        self.on_update = as_bool(options.get('on-update', 'false'))
        self.env = options.get('env')
        self.default_pkgs = split_args(options.get('default-pkgs', 'python'))
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
        create_env(self.anaconda_home, self.env, self.channels, self.default_pkgs)
        if not self.offline:
            install_pkgs(self.anaconda_home, self.env, self.channels, self.pkgs)
        
def uninstall(name, options):
    pass

