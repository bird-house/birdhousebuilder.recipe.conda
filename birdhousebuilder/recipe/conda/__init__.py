# -*- coding: utf-8 -*-

"""Recipe conda"""
import os
from os.path import join
import yaml
from subprocess import check_output, check_call

import logging

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

def conda_env_path(buildout, options):
    b_options = buildout['buildout']

    # get conda prefix from conda_env_path or anaconda_home
    conda_prefix = os.environ.get('CONDA_ENV_PATH', b_options.get('anaconda-home', '/opt/anaconda'))

    # use optional env
    env = options.get('env', b_options.get('conda-env'))
    if env:
        env_path = conda_envs(conda_prefix).get(env, conda_prefix)
    else:
        env_path = conda_prefix
    return env_path

def conda_info(prefix):
    """returns conda infos"""
    cmd = [join(prefix, 'bin', 'conda')]
    cmd.extend(['info', '--json'])
    output = check_output(cmd)
    return yaml.load(output)

def conda_envs(prefix):
    info = conda_info(prefix)
    env_names = [a_env.split('/')[-1] for a_env in info['envs']]
    return dict(zip(env_names, info['envs']))
    
def env_exists(prefix, env=None):
    """returns True if environment exists otherwise False."""
    return env in conda_envs(prefix)

class Recipe(object):
    """This recipe is used by zc.buildout.
    It install conda packages."""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']

        self.logger = logging.getLogger(self.name)

        # buildout option anaconda-home overwrites default conda env path
        self.anaconda_home = b_options.get('anaconda-home', '/opt/anaconda')
        b_options['anaconda-home'] = self.anaconda_home

        # conda prefix
        self.prefix = os.environ.get('CONDA_ENV_PATH', self.anaconda_home)
        
        # offline mode
        self.offline = as_bool(b_options.get('offline', 'false'))

        # channels option can be overwritten by buildout conda-channels option
        self.channels = split_args( options.get('channels', b_options.get('conda-channels', 'birdhouse')) )
        
        # make channel list unique
        self.channels = list(set(self.channels))
            
        # env option can be overwritten by buildout conda-env option
        self.env = options.get('env', b_options.get('conda-env'))
        self.default_pkgs = split_args(options.get('default-pkgs', 'python=2 pip'))
        self.pkgs = split_args(options.get('pkgs'))
        self.pip_pkgs = split_args(options.get('pip'))

    def install(self, update=False):
        """
        install conda packages
        """
        return self.execute(update=update)

    def update(self):
        return self.install(update=True)
    
    def execute(self, update=False):
        offline = self.offline or update
        self._create_env(self.prefix, self.env, self.channels, self.default_pkgs, offline)
        self._install_pkgs(self.prefix, self.env, self.channels, self.pkgs, offline)
        self._install_pip(self.prefix, self.env, self.pip_pkgs, offline)
        return tuple()

    def _create_env(self, prefix, env=None, channels=None, pkgs=None, offline=False, update_deps=True):
        if not env or env_exists(prefix, env) or not pkgs:
            return

        self.logger.info("Creating conda environment %s ...", env)

        cmd = [join(prefix, 'bin', 'conda')]
        cmd.extend(['create', '-n', env])
        if offline:
            cmd.append('--offline')
        if not update_deps:
            cmd.append('--no-update-deps')
        cmd.append('--yes')
        if channels:
            for channel in channels:
                cmd.extend(['-c', channel])
        cmd.extend(pkgs)
        check_call(cmd)
    
    def _install_pkgs(self, prefix, env=None, channels=None, pkgs=None, offline=False, update_deps=True):
        """
        TODO: maybe use offline option
        TODO: maybe use conda as python package
        """
        if pkgs:
            self.logger.info("Installing conda packages ...")
            cmd = [join(prefix, 'bin', 'conda')]
            cmd.append('install')
            if offline:
                cmd.append('--offline')
            if not update_deps:
                cmd.append('--no-update-deps')
            if env:
                self.logger.info("... in conda environment %s ...", env)
                cmd.extend(['-n', env])
            cmd.append('--yes')
            if channels:
                self.logger.info("... with conda channels: %s ...", ', '.join(channels))
                for channel in channels:
                    cmd.append('-c')
                    cmd.append(channel)
            cmd.extend(pkgs)
            check_call(cmd)
        return pkgs

    def _install_pip(self, prefix, env=None, pkgs=None, offline=False):
        if not offline and pkgs:
            envs = conda_envs(prefix)
            env_path = envs.get(env, prefix)

            self.logger.info("Installing pip packages in conda env path %s", env_path)

            cmd = [join(env_path, 'bin', 'pip')]
            cmd.append('install')
            cmd.extend(pkgs)
            check_call(cmd)
        return pkgs
        
def uninstall(name, options):
    pass

