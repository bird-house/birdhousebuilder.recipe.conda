# -*- coding: utf-8 -*-

"""Recipe conda"""
import os
from os.path import join
import yaml
from subprocess import check_output, check_call

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

def conda_info(anaconda_home):
    """returns conda infos"""
    cmd = [join(anaconda_home, 'bin', 'conda')]
    cmd.extend(['info', '--json'])
    output = check_output(cmd)
    return yaml.load(output)

def conda_envs(anaconda_home):
    info = conda_info(anaconda_home)
    env_names = [a_env.split('/')[-1] for a_env in info['envs']]
    return dict(zip(env_names, info['envs']))
    
def env_exists(anaconda_home, env=None):
    """returns True if environment exists otherwise False."""
    return env in conda_envs(anaconda_home)

def create_env(anaconda_home, env=None, channels=[], pkgs=['python=2 pip']):
    if not env or env_exists(anaconda_home, env):
        return
    
    cmd = [join(anaconda_home, 'bin', 'conda')]
    cmd.extend(['create', '-n', env])
    cmd.append('--yes')
    for channel in channels:
        cmd.append('-c')
        cmd.append(channel)
    cmd.extend(pkgs)
    check_call(cmd)

def install_pkgs(anaconda_home, env=None, channels=[], pkgs=[]):
    """
    TODO: maybe use offline option
    TODO: maybe use conda as python package
    """
    if len(pkgs) > 0:
        cmd = [join(anaconda_home, 'bin', 'conda')]
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

def install_pip(anaconda_home, env=None, pkgs=[]):
    if len(pkgs) > 0:
        envs = conda_envs(anaconda_home)
        env_path = envs.get(env, anaconda_home)
        cmd = [join(env_path, 'bin', 'pip')]
        cmd.append('install')
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
        
        self.channels = split_args( b_options.get('conda-channels', 'birdhouse') )
        self.channels.extend( split_args( options.get('channels')) )
        # make channel list unique
        self.channels = list(set(self.channels))
        self.on_update = as_bool(options.get('on-update', 'false'))
        self.env = options.get('env', b_options.get('conda-env'))
        self.default_pkgs = split_args(options.get('default-pkgs', 'python=2 pip'))
        self.pkgs = split_args(options.get('pkgs'))
        self.pip_pkgs = split_args(options.get('pip'))

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
            install_pip(self.anaconda_home, self.env, self.pip_pkgs)
        
def uninstall(name, options):
    pass

