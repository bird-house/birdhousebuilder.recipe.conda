# -*- coding: utf-8 -*-

"""Recipe conda"""
import os
from os.path import join
import yaml
from subprocess import check_output, check_call

from zc.buildout.buildout import bool_option

import logging

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
        self.offline = bool_option(b_options, 'offline', False)

        # newest mode
        self.newest = bool_option(b_options, 'newest', True)

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
        self._create_env(offline)
        self._install_pkgs(offline)
        self._install_pip(offline)
        return tuple()

    def _create_env(self, offline=False):
        if not self.env or env_exists(self.prefix, self.env) or not self.default_pkgs:
            return

        self.logger.info("Creating conda environment %s ...", self.env)

        cmd = [join(self.prefix, 'bin', 'conda')]
        cmd.extend(['create', '-n', self.env])
        if offline:
            cmd.append('--offline')
        if not self.newest:
            cmd.append('--no-update-deps')
        cmd.append('--yes')
        if self.channels:
            for channel in self.channels:
                cmd.extend(['-c', channel])
        cmd.extend(self.default_pkgs)
        check_call(cmd)
    
    def _install_pkgs(self, offline=False):
        """
        TODO: maybe use conda as python package
        """
        if self.pkgs:
            self.logger.info("Installing conda packages ...")
            cmd = [join(self.prefix, 'bin', 'conda')]
            cmd.append('install')
            if offline:
                cmd.append('--offline')
            if not self.newest:
                cmd.append('--no-update-deps')
            if self.env:
                self.logger.info("... in conda environment %s ...", self.env)
                cmd.extend(['-n', self.env])
            cmd.append('--yes')
            if self.channels:
                self.logger.info("... with conda channels: %s ...", ', '.join(self.channels))
                for channel in self.channels:
                    cmd.append('-c')
                    cmd.append(channel)
            cmd.extend(self.pkgs)
            check_call(cmd)
        return self.pkgs

    def _install_pip(self, offline=False):
        if not offline and self.pip_pkgs:
            envs = conda_envs(self.prefix)
            env_path = envs.get(self.env, self.prefix)

            self.logger.info("Installing pip packages in conda env path %s", env_path)

            cmd = [join(env_path, 'bin', 'pip')]
            cmd.append('install')
            cmd.extend(self.pip_pkgs)
            check_call(cmd)
        return self.pip_pkgs
        
def uninstall(name, options):
    pass

